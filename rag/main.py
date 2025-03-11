"""
FASTAPI APP 메인 파일
"""

import logging
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 현재 스크립트 위치의 부모 디렉토리(프로젝트 루트)를 경로에 추가
sys.path.append(str(Path(__file__).parent.parent))

# pylint: disable=wrong-import-position
from rag.api.gpt_routes import gpt_router
from rag.api.routes import router
from rag.core.config import settings
from rag.database.chroma_client import chroma_db

# pylint: enable=wrong-import-position

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    dotenv_path = (
        Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / ".env"
    )
    load_dotenv(dotenv_path=dotenv_path)

    if os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
except Exception as e:  # pylint: disable=broad-except
    logger.error("환경 변수 로드 실패: %s", e)


@asynccontextmanager
async def lifespan(app_instance: FastAPI):  # pylint: disable=unused-argument
    """
    앱의 수명 주기를 관리하는 컨텍스트 매니저
    """
    # 앱 시작 시 데이터베이스의 연결 초기화
    chroma_db.initialize()

    yield  # FastAPI 앱이 실행됨

    # 앱 종료 시 데이터베이스의 연결 종료
    chroma_db.close()


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
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
app.include_router(gpt_router, prefix="/api/gpt/v1")


@app.get("/", tags=["요청"])
async def root():
    """
    루트 경로 호출 시 반환되는 메시지
    """
    return {"message": "가전제품 RAG API 서버가 실행 중입니다", "api": "/api"}
