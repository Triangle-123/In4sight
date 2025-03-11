"""
1차 MVP API 라우터 모듈
"""

from fastapi import APIRouter, HTTPException

from ..database.chroma_client import chroma_db

router = APIRouter(tags=["검색"])


@router.get("/")
async def root():
    """
    루트 경로 호출 API
    """
    return {"message": "가전제품 RAG API입니다!"}


@router.get("/collections")
async def list_collections():
    """
    사용 가능한 컬렉션 목록을 반환하는 API
    """
    client = chroma_db.get_client()
    try:
        collections = client.list_collections()
        return {"collections": [col.name for col in collections]}
    except Exception as e:
        # from e: 발생한 예외를 새로운 예외의 __cause__ 속성에 저장한다.
        raise HTTPException(
            status_code=500, detail=f"컬렉션 목록 조회 실패: {str(e)}"
        ) from e
