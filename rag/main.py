"""
FASTAPI APP 메인 파일
"""

import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from prometheus_fastapi_instrumentator import Instrumentator
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 현재 스크립트 위치의 부모 디렉토리(프로젝트 루트)를 경로에 추가
sys.path.append(str(Path(__file__).parent.parent))

# pylint: disable=wrong-import-position
import eda

from rag.api.gpt_routes import gpt_router
from rag.api.routes import router
from rag.core.config import settings
from rag.core.loki import setup_logging
from rag.database.chroma_client import chroma_db
from rag.llm.rag_service import process_data_analysis_event


# pylint: enable=wrong-import-position

# 로깅 설정
logger = setup_logging()

try:
    dotenv_path = (
        Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / ".env"
    )
    load_dotenv(dotenv_path=dotenv_path)

    if os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    if os.getenv("KAFKA_BOOTSTRAP_SERVER"):
        os.environ["KAFKA_BOOTSTRAP_SERVER"] = os.getenv("KAFKA_BOOTSTRAP_SERVER")
    if os.getenv("LOKI_URL"):
        os.environ["LOKI_URL"] = os.getenv("LOKI_URL")
except Exception as e:  # pylint: disable=broad-except
    logger.error("환경 변수 로드 실패: %s", e)


@asynccontextmanager
async def lifespan(app_instance: FastAPI):  # pylint: disable=unused-argument
    """
    앱의 수명 주기를 관리하는 컨텍스트 매니저
    """
    # 앱 시작 시 데이터베이스의 연결 초기화
    chroma_db.initialize()

    # Kafka 컨슈머 초기화 및 이벤트 구독 설정
    try:
        bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVER"]
        group_id = "rag-server-group"

        # Kafka 컨슈머 생성
        eda.create_consumer(
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            enable_auto_commit=True,
        )

        eda.create_producer(bootstrap_servers=bootstrap_servers)

        # DAS 이벤트 구독
        eda.event_subscribe(
            group_id=group_id, topic="das_result", callback=process_data_analysis_event
        )

        logger.info("Kafka 이벤트 구독이 성공적으로 설정되었습니다.")
    except Exception as e:  # pylint: disable=broad-except
        logger.error("Kafka 이벤트 구독 설정 실패: %s", e)

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

# Setup Prometheus
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, include_in_schema=False)


@app.get("/", tags=["요청"])
async def root():
    """
    루트 경로 호출 시 반환되는 메시지
    """
    kafka_server = os.getenv("KAFKA_BOOTSTRAP_SERVER")

    eda.create_producer(kafka_server)
    eda.event_broadcast("data-analysis-completed", "ㅇㅇ")

    return {"message": "가전제품 RAG API 서버가 실행 중입니다", "api": "/api"}


@app.get("/health")
async def health():
    """
    서버 상태 확인 엔드포인트
    """
    logger.info("서버 상태 확인 엔드포인트 호출")
    return {"status": "ok"}
