"""
1차 MVP API 라우터 모듈
"""

import logging
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from rag.database.chroma_client import chroma_db
from rag.database.chroma_operation import ChromaDBOperations
from rag.llm.rag_service import process_data_analysis_event

logger = logging.getLogger(__name__)

router = APIRouter(tags=["검색"])
client = chroma_db.get_client()


class ApiResponse(BaseModel):
    """API 응답 기본 모델"""

    success: bool
    message: str
    data: Optional[Any] = None


class QueryRequest(BaseModel):
    """검색 요청 모델"""

    query_text: str
    n_results: int = 5
    where: Optional[Dict[str, Any]] = None
    where_document: Optional[Dict[str, Any]] = None
    query_embedding: Optional[List[float]] = None


# 요청 모델 정의
class DocumentInsertRequest(BaseModel):
    """
    ChromaDB 단일 데이터 삽입 스키마
    """

    document: str
    metadata: Optional[Dict[str, Any]] = None
    id: Optional[str] = None


class DocumentsInsertRequest(BaseModel):
    """
    ChromaDB 다중 데이터 삽입 스키마마
    """

    documents: List[str]
    metadatas: Optional[List[Dict[str, Any]]] = None
    ids: Optional[List[str]] = None


def get_db_ops(collection_name: str = Query("device")):
    """API 엔드포인트에서 사용할 ChromaDBOperations 인스턴스 제공"""
    try:
        return ChromaDBOperations(collection_name=collection_name)
    except Exception as e:
        logger.error("ChromaDB 연결 실패: %s", str(e))
        raise HTTPException(
            status_code=500, detail=f"데이터베이스 연결 오류: {str(e)}"
        ) from e


@router.get("/")
async def root():
    """
    루트 경로 호출 API
    """
    return {"message": "가전제품 RAG API입니다!"}


@router.post("/rag-test")
async def message_test(message: Dict[str, Any]):
    """
    RAG 기능 테스트
    """
    process_data_analysis_event(message)

    return {"message": "요청에 성공하셨습니다!"}


@router.get("/collections")
async def list_collections():
    """
    사용 가능한 컬렉션 목록을 반환하는 API
    """
    try:
        collections = client.list_collections()

        return {"collections": collections}
    except Exception as e:
        # from e: 발생한 예외를 새로운 예외의 __cause__ 속성에 저장한다.
        raise HTTPException(
            status_code=500, detail=f"컬렉션 목록 조회 실패: {str(e)}"
        ) from e


@router.post("/collections")
def create_collection(collection_name: str):
    """
    새로운 컬렉션을 추가하는 API 엔드포인트
    """
    try:
        # 기존에 같은 이름의 컬렉션이 있는지 확인
        if collection_name in client.list_collections():
            raise HTTPException(status_code=400, detail="이미 존재하는 컬렉션입니다.")

        # 새 컬렉션 추가
        client.create_collection(collection_name)
        return {"message": f"컬렉션 '{collection_name}'이 성공적으로 생성되었습니다."}

    except Exception as e:  # pylint: disable=broad-except
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/document", response_model=ApiResponse)
async def add_document(
    request: DocumentInsertRequest, db_ops: ChromaDBOperations = Depends(get_db_ops)
):
    """단일 문서를 ChromaDB에 추가"""
    try:
        doc_id = request.id or str(uuid.uuid4())

        db_ops.add_document(
            document=request.document, metadata=request.metadata, doc_id=doc_id
        )

        return {
            "success": True,
            "message": "문서가 추가되었습니다.",
            "data": {"id": doc_id},
        }
    except Exception as e:
        logger.error("문서 추가 중 오류 발생: {str(%d)}", e)
        raise HTTPException(status_code=500, detail=f"문서 추가 오류: {str(e)}") from e


@router.post("/documents", response_model=ApiResponse)
async def add_documents(
    request: DocumentsInsertRequest, db_ops: ChromaDBOperations = Depends(get_db_ops)
):
    """여러 문서를 ChromaDB에 추가"""
    try:
        if not request.documents:
            raise HTTPException(status_code=400, detail="문서 내용이 필요합니다.")

        # ID가 제공되지 않은 경우 자동 생성
        ids = request.ids or [str(uuid.uuid4()) for _ in range(len(request.documents))]

        db_ops.add_documents(
            documents=request.documents, metadatas=request.metadatas, ids=ids
        )

        return {
            "success": True,
            "message": f"{len(request.documents)}개 문서가 추가되었습니다.",
            "data": {"ids": ids},
        }
    except ValueError as ve:
        logger.error("입력값 오류: {str(%d)}", ve)
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as e:
        logger.error("문서 추가 중 오류 발생: {str(%d)}", e)
        raise HTTPException(status_code=500, detail=f"문서 추가 오류: {str(e)}") from e
