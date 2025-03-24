"""
OpenAI GPT API 클라이언트 모듈
"""

import json
import logging
import os

import requests

from rag.llm.gpt.gpt_config import GPTConfig

# 로깅 설정
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GPTClient:
    """OpenAI GPT API와 통신하는 클라이언트 클래스"""

    def __init__(self, api_key=None):
        """초기화 함수"""
        self.api_key = api_key or os.environ["OPENAI_API_KEY"]

    def generate_completion(
        self, messages, model=None, temperature=None, max_tokens=None
    ):
        """OpenAI Chat Completion API 호출 함수"""
        # 설정 값 적용
        model = model or GPTConfig.DEFAULT_MODEL
        temperature = (
            temperature if temperature is not None else GPTConfig.DEFAULT_TEMPERATURE
        )
        max_tokens = max_tokens or GPTConfig.DEFAULT_MAX_TOKENS

        # API 요청 데이터 준비
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            response = requests.post(
                GPTConfig.API_ENDPOINT,
                headers=headers,
                data=json.dumps(data),
                timeout=8000,
            )
            response.raise_for_status()  # HTTP 에러 체크
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 요청 오류: {e}")
            return {"error": str(e)}
