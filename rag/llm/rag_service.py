"""
RAG 서비스 모듈 - Kafka 이벤트 처리 및 RAG 로직
"""

import concurrent.futures
import json
import logging
import pprint
from typing import Any, Dict

# Kafka에 이벤트 발행 (프로듀서 로직 필요)
import eda
from eda.producer import get_producer

from rag.llm.gpt.gpt_client import GPTClient
from rag.llm.gpt.gpt_handler import GPTHandler

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def suggest_additional_questions(message: Dict[str, Any]) -> None:
    """
    상담사의 추가 질문 이벤트를 처리합니다.

    Args:
        message: Kafka 메시지 내용
    """
    try:
        logger.info("상담사 추가 질문 이벤트 수신: %s", message)

        # 메시지에서 필요한 데이터 내용 추출
        analysis_id = message.get("analysis_id")
        # user_query = message.get("user_query")
        # 어떤 추가 정보를 받을까?
        # 현재 어떤 제품에 대해 질문하고 있는지??? -> LLM 서버 토큰 줄이기
        # 해당 제품의 시계열 데이터를 바탕으로 DAS에서 '적당히' 분석해서 LLM에 던져주면, LLM을 통해 추론하는 방식도 괜찮을거 같긴 합니다.
        # 약간 챗봇 느낌

        if not analysis_id:
            logger.error("유효하지 않은 메시지 형식: analysis_id가 없습니다")
            return
    except Exception as e:  # pylint: disable=broad-except
        logger.error("추가 질문 이벤트 처리 중 오류 발생: %s", e, exc_info=True)


def process_symptom_with_rag(
    failure_item: Dict[str, Any], product_type: str, client: GPTClient
) -> Dict[str, Any]:
    """
    각 증상에 대해 RAG를 수행합니다.

    Args:
        failure_item: 고장 증상 정보 (failure, causes, related_sensor 포함)
        product_type: 제품 타입
        client: GPT 클라이언트

    Returns:
        RAG 처리 결과

    """

    try:
        print(failure_item)
        failure = failure_item.get("failure", "")
        causes = failure_item.get("causes", [])
        related_sensors = failure_item.get("related_sensor", [])

        logger.info("고장 증상 '%s'에 대한 RAG 처리 시작", failure)

        handler = GPTHandler(client=client)

        # ChromaDB 질의 데이터 구성
        query_data = {
            "query_text": failure,
            "n_results": 3,
            "where": {"product_type": product_type} if product_type else None,
            "query_embedding": None,
        }

        # RAG 완료 호출
        response = handler.rag_completion(
            query_data=query_data, causes=causes, related_sensors=related_sensors
        )

        if not response.get("success"):
            logger.error(
                "증상 '%s'에 대한 RAG 처리 실패: %s", failure, response.get("error")
            )
            raise Exception  # pylint: disable=broad-exception-raised

        logger.info(
            "고장 증상 '%s'에 대한 RAG 처리 완료 (%d개 원인 분석)", failure, len(causes)
        )

        return {
            "failure": failure,
            "cause": causes,
            "sensor": related_sensors,
            "solutions": response.get("result", ""),
        }
    except Exception as e:  # pylint: disable=broad-except
        logger.error(
            "고장 증상 '%s' 처리 중 오류 발생: %s",
            failure_item.get("failure", "알 수 없음"),
            str(e),
            exc_info=True,
        )
        return {
            "success": False,
            "error": str(e),
            "failure": failure_item.get("failure", "알 수 없음"),
        }


def process_data_analysis_event(message: Dict[str, Any]) -> None:
    """
    데이터 분석 완료 이벤트를 처리합니다.

    Args:
        message: Kafka 메시지 내용
    """
    try:
        logger.info("데이터 분석 완료 이벤트 수신: %s", message)

        if isinstance(message, str):
            try:

                message = json.loads(message)
            except json.JSONDecodeError:
                logger.error("메시지를 JSON으로 파싱할 수 없습니다: %s", message)
                return
        if isinstance(message, dict) and "data" in message:
            data = message["data"]
        else:
            data = message

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                logger.error("데이터를 JSON으로 파싱할 수 없습니다: %s", data)
                return

        # 메시지에서 필요한 데이터 추출
        serial_number = message.get("serialNumber")
        task_id = message.get("taskId")
        product_type = message.get("product_type")

        if not task_id:
            logger.error("유효하지 않은 메시지 형식: task_id가 없습니다")
            return

        client = GPTClient()

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(8, len(data))
        ) as executor:
            # For문 돌면서 스레드 풀에서 스레드 하나씩 가져오기
            future_to_symptom = {
                # 각 스레드별로 증상 하나씩 담당하여 작업하기
                executor.submit(
                    process_symptom_with_rag,  # Vector DB에 질의하고 LLM 추론 결과를 얻는 함수
                    symptom_item,
                    product_type,
                    client,
                ): symptom_item.get("failure", f"Item-{i}")
                for i, symptom_item in enumerate(data)
            }

            for future in concurrent.futures.as_completed(future_to_symptom):
                failure = future_to_symptom[future]

                try:
                    result = future.result()
                    publish_rag_completed_event(
                        task_id=task_id, result=result, serial_number=serial_number
                    )

                except Exception as e:  # pylint: disable=broad-except
                    logger.error(
                        "고장 증상 [%s] 처리 중 예외 발생: %s",
                        failure,
                        str(e),
                        exc_info=True,
                    )

        logger.info("RAG 분석 및 이벤트 발행 완료: %s", task_id)
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


def publish_rag_completed_event(task_id: str, result, serial_number: str) -> None:
    """
    RAG 분석 완료 이벤트를 Kafka에 발행합니다.

    Args:
        analysis_id: 분석 ID
        result: GPT 응답 결과
    """
    try:
        print("result 타입")
        print(result["solutions"])
        # DiagnosticResult 객체를 딕셔너리로 변환
        if "solutions" in result and isinstance(result["solutions"], list):
            result["solutions"] = [
                item.to_dict() if hasattr(item, "to_dict") else item
                for item in result["solutions"]
            ]

        event_data = {
            "taskId": task_id,
            "result": {"serial_number": serial_number, "data": result},
        }

        producer = get_producer()
        if producer:
            print("=============이벤트발행==============")
            eda.event_broadcast("rag-result", event_data)
            pprint.pprint(event_data)
            logger.info("RAG 분석 완료 이벤트가 성공적으로 발행되었습니다.")
        else:
            logger.error("Kafka 프로듀서가 설정되지 않았습니다.")
    except Exception as e:  # pylint: disable=broad-except
        logger.error("이벤트 발행 중 오류 발생: %s", e)
