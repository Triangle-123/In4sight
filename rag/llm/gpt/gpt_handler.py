"""
GPT 요청 및 응답 처리 모듈
"""

import logging

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from rag.database.chroma_operation import ChromaDBOperations
from rag.database.embedding_loader import embedding_loader
from rag.llm.gpt.util.similarity_utils import hybrid_similarity

from ..rag_response import DiagnosticResult
from .gpt_client import GPTClient
from .prompt.base_prompts import BasePrompts

logger = logging.getLogger(__name__)


class GPTHandler:
    """GPT 요청 처리 및 응답 관리 클래스"""

    def __init__(self, client=None):
        """초기화 함수"""
        self.client = client or GPTClient()
        self.db_ops = ChromaDBOperations(collection_name="device-test")

    def simple_completion(self, user_message, system_message):
        """간단한 메시지 완성 요청 처리 함수"""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]

        response = self.client.generate_completion(messages)

        # 응답 처리
        if "error" in response:
            return {"success": False, "error": response["error"]}

        try:
            content = response["choices"][0]["message"]["content"]

            try:
                diagnostic_result = DiagnosticResult.from_json(content)

                return {"success": True, "result": diagnostic_result}
            except ValueError as json_error:
                return {
                    "success": False,
                    "error": f"DTO 변환 오류: {str(json_error)}",
                    "raw_content": content,
                }
        except (KeyError, IndexError) as e:
            return {"success": False, "error": f"응답 파싱 오류: {str(e)}"}

    # pylint: disable=too-many-statements
    def rag_completion(
        self, query_data, causes, related_sensors, customer_history, event
    ):
        """
        RAG 기반 완성 요청 처리 함수 - 시맨틱 검색 적용

        Args:
            query_data (dict): 쿼리 데이터 딕셔너리
                - query_text (str): 사용자 쿼리 텍스트
                - n_results (int): 검색할 결과 수 (기본값: 3)
                - where (dict, optional): 메타데이터 필터링 조건
                - where_document (dict, optional): 문서 내용 필터링 조건
                - use_semantic_search (bool, optional): 시맨틱 검색 사용 여부 (기본값: True)
                - query_embedding (List[float], optional): 사전에 계산된 임베딩 벡터

        Returns:
            dict: LLM 응답 결과
        """
        # 쿼리 데이터에서 필요한 정보 추출
        query_text = query_data.get("query_text", "")
        n_results = query_data.get("n_results", 3)
        where = query_data.get("where")
        where_document = query_data.get("where_document")
        use_semantic_search = query_data.get("use_semantic_search", True)
        query_embedding = query_data.get("query_embedding")

        # 로깅
        logger.info(
            "RAG 완성 요청 처리 시작 - 쿼리: '%s'",
            query_text[:30] + "..." if len(query_text) > 30 else query_text,
        )

        # 임베딩 벡터가 없고 시맨틱 검색을 사용하는 경우 임베딩 생성
        if use_semantic_search and not query_embedding:
            try:
                logger.debug("쿼리 텍스트에 대한 임베딩 벡터 생성 중...")
                query_embedding = embedding_loader.encode([query_text])[0]
                logger.debug("임베딩 벡터 생성 완료")
            except Exception as e:  # pylint: disable=broad-except
                logger.error("임베딩 벡터 생성 중 오류 발생: %s", str(e))
                # 오류 발생시 시맨틱 검색 사용하지 않음
                use_semantic_search = False
                query_embedding = None

        # vectorDB 질의하기
        try:
            if use_semantic_search:
                # 시맨틱 검색 사용 (임베딩 사용)
                results = self.db_ops.query_documents(
                    query_text=query_text,
                    n_results=n_results,
                    where=where,
                    where_document=where_document,
                    query_embedding=query_embedding,
                )
                logger.info("시맨틱 검색 완료 (임베딩 벡터 사용)")

            else:
                # 기본 검색 사용 (텍스트 기반)
                results = self.db_ops.query_documents(
                    query_text=query_text,
                    n_results=n_results,
                    where=where,
                    where_document=where_document,
                )
                logger.info("기본 검색 완료")
        except Exception as e:  # pylint: disable=broad-except
            logger.error("문서 검색 중 오류 발생: %s", str(e))
            # 오류 발생 시 빈 결과 반환
            results = {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
            }

        # 필터링을 위한 빈 리스트 생성
        filtered_results = []
        filtered_metadatas = []
        filtered_distances = []
        filtered_ids = []
        similarity_scores = []

        # TF-IDF 벡터라이저 초기화
        all_texts = [query_text] + [
            metadata["title"] for metadata in results["metadatas"][0]
        ]
        vectorizer = TfidfVectorizer(min_df=1)
        vectorizer.fit(all_texts)

        # 결과에서 각 문서의 인덱스를 가져오기
        for i, (doc, metadata, distance, doc_id) in enumerate(
            zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
                results["ids"][0],
            )
        ):
            # 타이틀 임베딩 생성
            title_embedding = embedding_loader.encode([metadata["title"]])[0]
            print(metadata)
            # 하이브리드 유사도 계산
            similarity = hybrid_similarity(
                query_text,
                metadata["title"],
                query_embedding,
                title_embedding,
                embedding_weight=0.4,  # 임베딩 유사도 가중치
                keyword_weight=0.3,  # 키워드 매칭 가중치
                tfidf_weight=0.3,  # TF-IDF 유사도 가중치
                vectorizer=vectorizer,
            )

            print(
                f"쿼리: {query_text}, 제목: {metadata['title']}, 하이브리드 유사도: {similarity}"
            )

            # 임계값 이상인 항목만 포함
            if similarity >= 0.60:
                filtered_results.append(doc)
                filtered_metadatas.append(metadata)
                filtered_distances.append(distance)
                filtered_ids.append(doc_id)
                similarity_scores.append(similarity)

        # 유사도 점수에 따라 결과 재정렬
        if similarity_scores:
            # 내림차순으로 정렬하기 위한 인덱스 배열 생성
            sorted_indices = np.argsort(similarity_scores)[::-1]

            # 정렬된 결과 생성
            filtered_results = [filtered_results[i] for i in sorted_indices]
            filtered_metadatas = [filtered_metadatas[i] for i in sorted_indices]
            filtered_distances = [filtered_distances[i] for i in sorted_indices]
            filtered_ids = [filtered_ids[i] for i in sorted_indices]

        # 새로운 결과 객체 생성
        filtered_output = {
            "documents": [filtered_results[:n_results]],  # 원하는 결과 수만큼만 반환
            "metadatas": [filtered_metadatas[:n_results]],
            "distances": [filtered_distances[:n_results]],
            "ids": [filtered_ids[:n_results]],
            "included": results["included"],
            "data": None,
            "embeddings": None,
            "uris": None,
        }

        # 만약 필터링된 결과가 없다면 메시지 출력
        if not filtered_results:
            print("임계값을 넘는 결과가 없습니다.")

        # 검색 결과 처리 및 포맷팅
        context_str = self._format_search_results(filtered_output)

        # 프롬프트 구성
        user_message = BasePrompts.format_rag_prompt(
            context=context_str,
            query=query_text,
            causes=causes,
            related_sensors=related_sensors,
            customer_history=customer_history,
            event=event,
        )
        print("=========프롬프트!=========")
        print(user_message)
        system_message = BasePrompts.DIAGNOSTIC_SYSTEM

        # LLM에 완성 요청
        logger.info("LLM 완성 요청 시작")
        response = self.simple_completion(user_message, system_message)
        logger.info("RAG 완성 처리 완료")

        return response

    def _format_search_results(self, results):
        """
        검색 결과를 컨텍스트 문자열로 포맷팅

        Args:
            results (dict): query_documents 함수의 반환 결과

        Returns:
            str: 포맷팅된 컨텍스트 문자열
        """
        context_parts = []

        if not results or "documents" not in results or not results["documents"]:
            return "검색 결과가 없습니다."

        documents = results.get("documents", [[]])[0]
        metadatas = (
            results.get("metadatas", [[]])[0]
            if "metadatas" in results
            else [None] * len(documents)
        )
        distances = (
            results.get("distances", [[]])[0]
            if "distances" in results
            else [None] * len(documents)
        )

        for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
            # 메타데이터 문자열 구성
            meta_str = ""
            if meta:
                # 필요한 메타데이터 필드만 표시
                relevant_meta = {}
                for k, v in meta.items():
                    if k not in ["solution"]:  # solution은 별도로 처리
                        relevant_meta[k] = v

                meta_items = [f"{k}: {v}" for k, v in relevant_meta.items()]
                meta_str = f"[{', '.join(meta_items)}]"

            score_str = f"(유사도: {dist:.4f})" if dist is not None else ""

            # 문서 내용 구성
            document_content = doc
            if meta and "solution" in meta and meta["solution"].strip():
                title = meta.get("title", "")
                if title:
                    document_content = f"제목: {title}\n\n{meta['solution']}"
                else:
                    document_content = meta["solution"]

            doc_str = f"--- 문서 {i+1} {meta_str} {score_str} ---\n{document_content}\n"
            context_parts.append(doc_str)

        return "\n".join(context_parts)
