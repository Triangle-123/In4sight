"""
FASTAPI APP 메인 파일
"""

import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .core.config import settings
from .database.chroma_client import chroma_db

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# API 라우터 포함
app.include_router(router, prefix="/api")


@app.get("/", tags=["요청"])
async def root():
    """
    루트 경로 호출 시 반환되는 메시지
    """
    return {"message": "가전제품 RAG API 서버가 실행 중입니다", "api": "/api"}


# 앱 시작시 발생하는 이벤트 핸들러
@app.on_event("startup")
async def startup_db_client():
    """
    앱 시작 시 데이터베이스의 연결을 초기화하는 메소드
    """
    chroma_db.initialize()


# 앱 종료시 발생하는 이벤트 핸들러
@app.on_event("shutdown")
async def shutdown_db_client():
    """
    앱 종료 시 데이터베이스의 연결을 종료하는 메소드
    """
    chroma_db.close()
