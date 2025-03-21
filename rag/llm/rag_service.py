"""
RAG 서비스 모듈 - Kafka 이벤트 처리 및 RAG 로직
"""

import datetime
import logging
from typing import Any, Dict

# Kafka에 이벤트 발행 (프로듀서 로직 필요)
from eda.producer import event_broadcast, get_producer

from rag.llm.gpt.gpt_client import GPTClient
from rag.llm.gpt.gpt_handler import GPTHandler

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_data_analysis_event(message: Dict[str, Any]) -> None:
    """
    데이터 분석 완료 이벤트를 처리합니다.

    Args:
        message: Kafka 메시지 내용
    """
    try:
        logger.info("데이터 분석 완료 이벤트 수신: %s", message)

        # 메시지에서 필요한 데이터 추출
        analysis_id = message.get("analysis_id")
        product_type = message.get("product_type")
        analysis_results = message.get("results", {})

        if not analysis_id:
            logger.error("유효하지 않은 메시지 형식: analysis_id가 없습니다")
            return

        # GPT 클라이언트 및 핸들러 초기화
        client = GPTClient()
        handler = GPTHandler(client=client)

        # RAG 기반 GPT 완성 요청
        query_data = {
            "query_text": generate_query_from_analysis(analysis_results),
            "n_results": 5,
            "where": {"product_type": product_type} if product_type else None,
            "query_embedding": None,
        }

        response = handler.rag_completion(query_data=query_data)

        if not response.get("success"):
            logger.error("RAG 처리 실패: %s", response.get("error"))
            return

        # RAG 분석 완료 이벤트 발행
        publish_rag_completed_event(analysis_id, response.get("content", ""))

        logger.info("RAG 분석 및 이벤트 발행 완료: %s", analysis_id)
    except Exception as e:  # pylint: disable=broad-except
        logger.error("RAG 처리 중 오류 발생: %s", e, exc_info=True)


def generate_query_from_analysis(analysis_results: Dict[str, Any]) -> str:
    """
    데이터 분석 결과를 바탕으로 질의문을 생성합니다.

    Args:
        analysis_results: 데이터 분석 결과

    Returns:
        생성된 질의문 문자열
    """
    # 분석 결과에서 중요 정보 추출 및 질의문 생성
    summary = analysis_results.get("summary", "")
    issues = analysis_results.get("issues", [])

    query = f"가전제품 데이터 분석 결과: {summary}"

    if issues:
        issues_text = ", ".join(issues)
        query += f" 발견된 문제점: {issues_text}. 이 문제들에 대한 해결책과 추가 정보를 제공해주세요."

    return query


def publish_rag_completed_event(analysis_id: str, result: str) -> None:
    """
    RAG 분석 완료 이벤트를 Kafka에 발행합니다.

    Args:
        analysis_id: 분석 ID
        result: GPT 응답 결과
    """
    try:
        # 이벤트 데이터 구성
        event_data = {
            "event": "rag-result",
            "analysis_id": analysis_id,
            "result": result,
            "timestamp": datetime.datetime.now().isoformat(),
        }

        producer = get_producer()
        if producer:
            event_broadcast("rag-result", event_data)
            logger.info("RAG 분석 완료 이벤트가 성공적으로 발행되었습니다.")
        else:
            logger.error("Kafka 프로듀서가 설정되지 않았습니다.")
    except Exception as e:  # pylint: disable=broad-except
        logger.error("이벤트 발행 중 오류 발생: %s", e)
