"""
GPT API 테스트용 라우터 모듈
"""

import logging
import traceback

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from rag.llm.gpt.gpt_client import GPTClient
from rag.llm.gpt.gpt_handler import GPTHandler

gpt_router = APIRouter(
    tags=["CHAT GPT"],
)

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GPTRequest(BaseModel):
    """
    GPT 요청을 위한 Pydantic 모델(Data Transfer Object Class)
    """

    query: str
    product_type: str
    related_sensor: str


@gpt_router.post("/")
async def test_gpt(request: GPTRequest):
    """
    GPT API 테스트를 위한 API
    """
    try:
        client = GPTClient()
        logger.debug("GPTClient 초기화 성공")

        handler = GPTHandler(client=client)
        logger.debug("GPTHandler 초기화 성공")

        # 일반 GPT 완성 요청
        response = handler.simple_completion(
            user_message=request.query, system_message=request.system_message
        )

        if not response.get("success"):
            raise HTTPException(
                status_code=500,
                detail=response.get("error", "알 수 없는 오류가 발생했습니다."),
            )

        return {"response": response.get("content"), "usage": response.get("usage", {})}
    except Exception as e:  # pylint: disable=broad-except
        print(f"GPTClient 초기화 중 오류 발생: {type(e).__name__}: {str(e)}")
        print(traceback.format_exc())


@gpt_router.post("/rag")
async def test_gpt_rag(request: GPTRequest):
    """
    RAG 기반 GPT API 테스트를 위한 API
    """

    try:
        client = GPTClient()
        handler = GPTHandler(client=client)

        # RAG 기반 GPT 완성 요청
        query_data = {
            "query_text": request.query,
            "n_results": 10,
            "where": {"product_type": request.product_type},
            "query_embedding": None,
        }
        response = handler.rag_completion(query_data=query_data)

        if not response.get("success"):
            raise HTTPException(
                status_code=500,
                detail=response.get("error", "알 수 없는 오류가 발생했습니다."),
            )

        return {"response": response, "usage": response.get("usage", {})}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"RAG GPT 요청 처리 중 오류 발생: {str(e)}"
        ) from e
