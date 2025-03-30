"""
FastAPI 서버를 올리기 위한 main.py
"""

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.lifespan import lifespan
from app.loki import setup_logging

app = FastAPI(lifespan=lifespan)

# Setup Loki logging
logger = setup_logging()

# Setup Prometheus
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, include_in_schema=False)


@app.get("/api/v1/health", description="API status check", tags=["Common"])
def check_health():
    """
    API 헬스 체크 엔드포인트

    Returns:
        dict: API 상태 정보
    """
    logger.info("헬스 체크 API가 호출되었습니다.")
    return {"status": "OK"}
