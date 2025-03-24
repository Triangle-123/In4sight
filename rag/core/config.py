"""
앱 설정 관리 모듈
"""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    애플리케이션 설정
    """

    APP_TITLE: str = "가전제품 RAG API"
    APP_DESCRIPTION: str = "데이터 분석 결과로부터 가전제품 메뉴얼 검색 API"
    APP_VERSION: str = "0.1.0"

    # CORS 관련 설정
    CORS_ORIGINS: List[str] = ["*"]
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    # ChromaDB 관련 설정
    CHROMA_MAX_CONNECTION_AGE: int = 3600  # 1시간

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "allow",  # 추가 필드 허용
    }


# 설정 인스턴스 생성
settings = Settings()
