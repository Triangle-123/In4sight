"""
GPT 요청 및 응답 처리 모듈
"""

from rag.database.chroma_operation import ChromaDBOperations

from ..rag_response import DiagnosticResult
from .gpt_client import GPTClient
from .prompt.base_prompts import BasePrompts


class GPTHandler:
    """GPT 요청 처리 및 응답 관리 클래스"""

    def __init__(self, client=None):
        """초기화 함수"""
        self.client = client or GPTClient()
        self.db_ops = ChromaDBOperations(collection_name="device")

    def simple_completion(self, user_message, system_message):
        """간단한 메시지 완성 요청 처리 함수"""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]

        response = self.client.generate_completion(messages)

        # 응답 처리
        if "error" in response:
            return {"success": False, "error": response["error"]}

        try:
            content = response["choices"][0]["message"]["content"]
            usage = response.get("usage", {})

            try:
                diagnostic_result = DiagnosticResult.from_json(content)

                return {"success": True, "result": diagnostic_result, "usage": usage}
            except ValueError as json_error:
                return {
                    "success": False,
                    "error": f"DTO 변환 오류: {str(json_error)}",
                    "raw_content": content,
                }
        except (KeyError, IndexError) as e:
            return {"success": False, "error": f"응답 파싱 오류: {str(e)}"}

    def rag_completion(self, query_data):
        """RAG 기반 완성 요청 처리 함수"""
        # vectorDB 질의하기
        results = self.db_ops.query_documents(
            query_text=query_data["query_text"],
            n_results=query_data["n_results"],
            where=query_data["where"],
            query_embedding=query_data["query_embedding"],
        )

        user_message = BasePrompts.format_rag_prompt(
            context=results, query=query_data["query_text"]
        )
        system_message = BasePrompts.DIAGNOSTIC_SYSTEM

        return self.simple_completion(user_message, system_message)
