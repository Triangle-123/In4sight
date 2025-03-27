"""
GPT 요청 및 응답 처리 모듈
"""

import logging

from rag.database.chroma_operation import ChromaDBOperations
from rag.database.embedding_loader import embedding_loader

from ..rag_response import DiagnosticResult
from .gpt_client import GPTClient
from .prompt.base_prompts import BasePrompts

logger = logging.getLogger(__name__)


class GPTHandler:
    """GPT 요청 처리 및 응답 관리 클래스"""

    def __init__(self, client=None):
        """초기화 함수"""
        self.client = client or GPTClient()
        self.db_ops = ChromaDBOperations(collection_name="device")

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

    def rag_completion(self, query_data, causes, related_sensors):
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

        # 검색 결과 처리 및 포맷팅
        context_str = self._format_search_results(results)

        # 프롬프트 구성
        user_message = BasePrompts.format_rag_prompt(
            context=context_str,
            query=query_text,
            causes=causes,
            related_sensors=related_sensors,
        )
        system_message = BasePrompts.DIAGNOSTIC_SYSTEM

        # LLM에 완성 요청
        logger.info("LLM 완성 요청 시작")
        print(user_message)
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
                meta_items = [f"{k}: {v}" for k, v in meta.items()]
                meta_str = f"[{', '.join(meta_items)}]"

            # 유사도 점수 (있는 경우)
            score_str = f"(유사도: {dist:.4f})" if dist is not None else ""

            # 개별 문서 포맷팅
            doc_str = f"--- 문서 {i+1} {meta_str} {score_str} ---\n{doc}\n"
            context_parts.append(doc_str)

        # 전체 컨텍스트 문자열 결합
        return "\n".join(context_parts)
