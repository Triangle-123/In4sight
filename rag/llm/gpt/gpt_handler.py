"""
GPT 요청 및 응답 처리 모듈
"""

from .gpt_client import GPTClient
from .prompt.base_prompts import BasePrompts


class GPTHandler:
    """GPT 요청 처리 및 응답 관리 클래스"""

    def __init__(self, client=None):
        """초기화 함수"""
        self.client = client or GPTClient()

    def simple_completion(self, user_message, system_message=None):
        """간단한 메시지 완성 요청 처리 함수"""
        system_message = system_message or BasePrompts.SYSTEM_DEFAULT

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]

        response = self.client.generate_completion(messages)

        # 응답 처리
        if "error" in response:
            return {"success": False, "error": response["error"]}

        try:
            return {
                "success": True,
                "content": response["choices"][0]["message"]["content"],
                "usage": response.get("usage", {}),
            }
        except (KeyError, IndexError) as e:
            return {"success": False, "error": f"응답 파싱 오류: {str(e)}"}

    def rag_completion(self, query, context):
        """RAG 기반 완성 요청 처리 함수"""
        system_message = BasePrompts.DIAGNOSTIC_SYSTEM
        user_message = BasePrompts.format_rag_prompt(context, query)

        return self.simple_completion(user_message, system_message)
