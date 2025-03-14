"""
ChromaDB 데이터 관리 모듈
"""

import logging
from typing import Any, Dict, List, Optional

from rag.database.chroma_client import chroma_db

# 로깅 설정
logger = logging.getLogger(__name__)


class ChromaDBOperations:
    """
    ChromaDB에서 CRUD를 수행하는 클래스
    """

    def __init__(self, collection_name: str = "device"):
        """
        ChromaDB 작업을 위한 클래스 초기화

        Args:
            collection_name (str): 사용할 컬렉션 이름
        """
        self.collection_name = collection_name
        self._collection = None

    @property
    def collection(self):
        """
        ChromaDB 컬렉션을 가져오는 프로퍼티
        컬렉션이 없으면 생성하고, 있으면 기존 컬렉션을 반환
        """
        if self._collection is None:
            try:
                client = chroma_db.get_client()
                # DB에 해당 컬렉션이 있으면 가져오고 아니면 새로 생성
                self._collection = client.get_or_create_collection(
                    name=self.collection_name
                )
                logger.info("컬렉션 '%s'에 연결됨", self.collection_name)
            except Exception as e:
                logger.error("컬렉션 '%s' 연결 실패: %s", self.collection_name, str(e))
                raise
        return self._collection

    def query_documents(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None,
        query_embedding: Optional[List[float]] = None,
    ) -> Dict[str, Any]:
        """
        ChromaDB에서 문서 검색

        Args:
            query_text (str): 검색 쿼리 (query_embedding이 제공되지 않은 경우 사용)
            n_results (int): 반환할 결과 수
            where (dict, optional): 메타데이터 기반 필터링
            where_document (dict, optional): 문서 내용 기반 필터링
            query_embedding (List[float], optional): 사전 계산된 쿼리 임베딩 벡터

        Returns:
            dict: 검색 결과
        """
        try:
            logger.debug(
                "'%s' 쿼리로 문서 검색 시작",
                query_text[:30] + "..." if len(query_text) > 30 else query_text,
            )

            if query_embedding:
                result = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=n_results,
                    where=where,
                    where_document=where_document,
                )
            else:
                result = self.collection.query(
                    query_texts=[query_text],
                    n_results=n_results,
                    where=where,
                    where_document=where_document,
                )

            logger.info(
                "쿼리 검색 완료, %d개 결과 반환됨", len(result.get("ids", [[]])[0])
            )
            return result
        except Exception as e:
            logger.error("문서 검색 중 오류 발생: %s", str(e))
            raise

    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        ID로 문서 가져오기

        Args:
            document_id (str): 가져올 문서의 ID

        Returns:
            dict: 문서 정보 또는 없으면 None
        """
        try:
            logger.debug("문서 ID '%s' 조회 시작", document_id)

            result = self.collection.get(ids=[document_id])

            if result and result["ids"] and result["ids"][0]:
                document_data = {
                    "id": result["ids"][0],
                    "document": result["documents"][0] if result["documents"] else None,
                    "metadata": result["metadatas"][0] if result["metadatas"] else None,
                }

                # embeddings가 있는 경우에만 포함
                if "embeddings" in result and result["embeddings"]:
                    document_data["embedding"] = result["embeddings"][0]

                logger.info("문서 ID '%s' 조회 완료", document_id)
                return document_data

            logger.warning("문서 ID '%s'를 찾을 수 없음", document_id)
            return None
        except Exception as e:
            logger.error("문서 조회 중 오류 발생: %s", str(e))
            raise

    def get_documents(
        self,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None,
        ids: Optional[List[str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        include: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        여러 문서 가져오기 (필터링 옵션 포함)

        Args:
            where (dict, optional): 메타데이터 기반 필터링
            where_document (dict, optional): 문서 내용 기반 필터링
            ids (list, optional): 가져올 문서 ID 리스트
            limit (int, optional): 반환할 최대 문서 수
            offset (int, optional): 건너뛸 문서 수
            include (list, optional): 포함할 데이터 ('embeddings', 'metadatas', 'documents')

        Returns:
            dict: 문서 정보들
        """
        try:
            filter_desc = []
            if where:
                filter_desc.append(f"메타데이터 필터: {where}")
            if where_document:
                filter_desc.append(f"문서 필터: {where_document}")
            if ids:
                filter_desc.append(f"ID 필터: {len(ids)}개 ID")

            log_msg = (
                "모든 문서 조회 시작"
                if not filter_desc
                else f"필터링된 문서 조회 시작 ({', '.join(filter_desc)})"
            )
            logger.debug(log_msg)

            result = self.collection.get(
                where=where,
                where_document=where_document,
                ids=ids,
                limit=limit,
                offset=offset,
                include=include,
            )

            logger.info("문서 조회 완료, %d개 문서 반환됨", len(result.get("ids", [])))
            return result
        except Exception as e:
            logger.error("문서 조회 중 오류 발생: %s", str(e))
            raise

    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
        embeddings: Optional[List[List[float]]] = None,
    ) -> Dict[str, Any]:
        """
        여러 문서 추가하기

        Args:
            documents (List[str]): 추가할 문서 목록
            metadatas (List[Dict], optional): 문서별 메타데이터
            ids (List[str], optional): 문서별 고유 ID (제공하지 않으면 자동 생성됨)
            embeddings (List[List[float]], optional): 문서별 임베딩 (제공하지 않으면 자동 생성됨)

        Returns:
            dict: 추가된 문서 정보
        """
        try:
            if not documents:
                logger.warning("추가할 문서가 없습니다.")
                return {"ids": []}

            # 메타데이터, ID가 없으면 None으로 처리 (ChromaDB가 자동 생성)
            doc_count = len(documents)

            if metadatas and len(metadatas) != doc_count:
                logger.warning(
                    "문서 수와 메타데이터 수가 일치하지 않습니다: %d vs %d",
                    doc_count,
                    len(metadatas),
                )
                raise ValueError("문서 수와 메타데이터 수가 일치해야 합니다")

            if ids and len(ids) != doc_count:
                logger.warning(
                    "문서 수와 ID 수가 일치하지 않습니다: %d vs %d", doc_count, len(ids)
                )
                raise ValueError("문서 수와 ID 수가 일치해야 합니다")

            if embeddings and len(embeddings) != doc_count:
                logger.warning(
                    "문서 수와 임베딩 수가 일치하지 않습니다: %d vs %d",
                    doc_count,
                    len(embeddings),
                )
                raise ValueError("문서 수와 임베딩 수가 일치해야 합니다")

            # 로깅
            log_msg = f"{doc_count}개 문서 추가 시작"
            if ids:
                log_msg += f" (ID 제공됨: {ids[:3]}{'...' if len(ids) > 3 else ''})"
            logger.debug(log_msg)

            # ChromaDB에 문서 추가
            result = self.collection.add(
                documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings
            )

            logger.info("문서 추가 완료, %d개 문서 추가됨", doc_count)
            return result
        except Exception as e:
            logger.error("문서 추가 중 오류 발생: %s", str(e))
            raise

    def add_document(
        self,
        document: str,
        metadata: Optional[Dict[str, Any]] = None,
        doc_id: Optional[str] = None,
        embedding: Optional[List[float]] = None,
    ) -> Dict[str, Any]:
        """
        단일 문서 추가하기 (add_documents의 편의 래퍼)

        Args:
            document (str): 추가할 문서
            metadata (Dict, optional): 문서 메타데이터
            doc_id (str, optional): 문서 고유 ID (제공하지 않으면 자동 생성됨)
            embedding (List[float], optional): 문서 임베딩 (제공하지 않으면 자동 생성됨)

        Returns:
            dict: 추가된 문서 정보
        """
        documents = [document]
        metadatas = [metadata] if metadata else None
        ids = [doc_id] if doc_id else None
        embeddings = [embedding] if embedding else None

        return self.add_documents(
            documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings
        )
