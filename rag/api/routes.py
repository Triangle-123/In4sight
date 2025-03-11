"""
1차 MVP API 라우터 모듈
"""

from fastapi import APIRouter, HTTPException

from rag.database.chroma_client import chroma_db

router = APIRouter(tags=["검색"])
client = chroma_db.get_client()


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
