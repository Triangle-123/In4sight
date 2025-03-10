"""
FASTAPI APP 메인 파일
"""

import logging
import time

import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 글로벌 변수 선언
_CHROMA_CLIENT = None
_LAST_CONNECTION_TIME = 0
_MAX_CONNECTION_AGE = 3600  # 1시간마다 연결 갱신 검토

app = FastAPI(
    title="가전제품 RAG API",
    description="데이터 분석 결과로부터 가전제품 메뉴얼 검색 API",
    version="0.1.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["요청"])
async def root():
    """
    루트 경로 호출 시 반환되는 메시지
    """
    return {"message": "Hello World"}


def get_chroma_client() -> chromadb.Client:
    """
    데이터베이스 연결 관리 함수
    """
    # pylint: disable=global-statement
    global _CHROMA_CLIENT, _LAST_CONNECTION_TIME
    current_time = time.time()  # 현재 요청한 시각

    # 클라이언트가 없거나 너무 오래된 연결이면 재연결을 검토한다.
    if (
        _CHROMA_CLIENT is None
        or (current_time - _LAST_CONNECTION_TIME) > _MAX_CONNECTION_AGE
    ):
        try:
            # 기존 연결이 있으면 상태를 확인한다.
            if _CHROMA_CLIENT is not None:
                try:
                    # 연결 상태를 확인한다 (간단한 쿼리 실행)
                    _CHROMA_CLIENT.list_collections()
                    # 연결이 정상이면 타임스탬프만 갱신한다.
                    _LAST_CONNECTION_TIME = current_time
                    return _CHROMA_CLIENT
                except Exception as conn_err:  # pylint: disable=broad-except
                    logger.warning(
                        "ChromaDB 연결 오류 감지: %s, 재연결 시도...", str(conn_err)
                    )

            # 새 클라이언트를 생성한다.
            _CHROMA_CLIENT = chromadb.Client()
            # 마지막 연결 시각을 갱신한다.
            _LAST_CONNECTION_TIME = current_time
            logger.info("ChromaDB 새 연결 수립 완료")
        except Exception as e:  # pylint: disable=broad-except
            logger.error("ChromaDB 연결 실패: %s", str(e))
            if _CHROMA_CLIENT is None:
                raise ConnectionError("ChromaDB에 연결할 수 없습니다") from e

    return _CHROMA_CLIENT


# 앱 시작시 발생하는 이벤트 핸들러
@app.on_event("startup")
async def startup_db_client():
    """
    앱 시작 시 데이터베이스의 연결을 초기화하는 메소드
    """
    try:
        get_chroma_client()
        logger.info("ChromaDB 연결 초기화 완료")
    except ConnectionError as e:
        logger.error("ChromaDB 초기 연결 실패: %s", str(e))


# 앱 종료시 발새하는는 이벤트 핸들러
@app.on_event("shutdown")
async def shutdown_db_client():
    """
    앱 종료 시 데이터베이스의 연결을 종료하는 메소드
    """
    # pylint: disable=global-statement
    global _CHROMA_CLIENT
    _CHROMA_CLIENT = None
    logger.info("ChromaDB 연결 종료")
