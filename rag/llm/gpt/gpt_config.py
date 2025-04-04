"""
GPT API 설정 관리 모듈
"""

import logging

# 로깅 설정
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GPTConfig:
    """GPT API 설정 관리 클래스"""

    # 기본 모델 설정
    DEFAULT_MODEL = "gpt-4o"

    # API 요청 기본 설정
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 1000

    # API 엔드포인트
    API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
