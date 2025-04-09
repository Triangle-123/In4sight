"""
RAG 서비스 모듈 - Kafka 이벤트 처리 및 RAG 로직
"""

import concurrent.futures
import json
import logging
import pprint
import time
from multiprocessing import Manager
from typing import Any, Dict

# Kafka에 이벤트 발행 (프로듀서 로직 필요)
import eda
from eda.producer import get_producer

from rag.llm.gpt.gpt_client import GPTClient
from rag.llm.gpt.gpt_handler import GPTHandler
from rag.llm.rag_response import DiagnosticResult

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

manager = Manager()
customer_log_dict = manager.dict()


def process_counseling_history_event(
    message: Any,
) -> None:
    """
    고객의 과거 상담 이력 정보를 받아 캐싱합니다.
    """

    logger.info("고객 상담 이력 정보 수신")
    if not message:
        logger.error("유효하지 않은 메시지 형식: message가 없습니다")
        return

    pprint.pprint(message)
    # 첫 번째 키를 가져옵니다
    task_id = message.get("taskId")

    # 스레드 안전하게 딕셔너리에 값을 저장합니다
    customer_log_dict[task_id] = message


def process_symptom_with_rag(
    failure_item: Dict[str, Any],
    product_type: str,
    client: GPTClient,
    task_id: str,
) -> Dict[str, Any]:
    """
    각 증상에 대해 RAG를 수행합니다.

    Args:
        failure_item: 고장 증상 정보 (failure, causes, related_sensor 포함)
        product_type: 제품 타입
        client: GPT 클라이언트
        task_id: 작업 아이디

    Returns:
        RAG 처리 결과

    """

    try:
        failure = failure_item.get("failure", "")
        causes = failure_item.get("causes", [])
        related_sensors = failure_item.get("related_sensor", [])
        related_sensor_en = failure_item.get("related_sensor_en", [])
        event = failure_item.get("event", [])
        logger.info("고장 증상 '%s'에 대한 RAG 처리 시작", failure)

        handler = GPTHandler(client=client)

        # ChromaDB 질의 데이터 구성
        query_data = {
            "query_text": failure,
            "n_results": 3,
            "where": {"product_type": product_type} if product_type else None,
            "query_embedding": None,
        }

        customer_history = customer_log_dict.get(task_id)

        response = handler.rag_completion(
            query_data=query_data,
            causes=causes,
            related_sensors=related_sensors,
            customer_history=customer_history,
            event=event,
        )

        if not response.get("success"):
            logger.error(
                "증상 '%s'에 대한 RAG 처리 실패: %s", failure, response.get("error")
            )
            raise Exception  # pylint: disable=broad-exception-raised

        logger.info(
            "고장 증상 '%s'에 대한 RAG 처리 완료 (%d개 원인 분석)", failure, len(causes)
        )

        # DiagnosticResult 객체를 딕셔너리로 변환
        result = response.get("result", "")
        if isinstance(result, DiagnosticResult):
            result = result.to_dict()

        return {
            "failure": failure,
            "cause": causes,
            "sensor": related_sensors,
            "related_sensor_en": related_sensor_en,
            "solutions": result,
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


# pylint: disable=too-many-branches, too-many-statements
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

        # customer_log_dict에서 task_id를 통해 customer_history 가져오기 (최대 5번 시도)
        retry_count = 0
        max_retries = 5
        wait_time = 1.5  # 초 단위 대기 시간

        customer_history = None
        customer_id = None
        counseling_date = None

        while retry_count < max_retries:
            # 락 없이 직접 딕셔너리에 접근 (manager.dict()는 내부적으로 동기화 처리)
            customer_history = customer_log_dict.get(task_id)
            if customer_history is not None:
                customer_id = customer_history.get("customerId")
                counseling_date = customer_history.get("counselingDate")

                # 모든 필요한 데이터가 존재하는지 확인
                if customer_id is not None and counseling_date is not None:
                    break

            logger.info(
                "customer_history 데이터가 완전하지 않습니다. %s번째 재시도 중... (대기 %s초)",
                retry_count,
                wait_time,
            )
            time.sleep(wait_time)
            retry_count += 1

        if customer_history is None or customer_id is None or counseling_date is None:
            logger.warning(
                "최대 재시도 횟수(%s)를 초과했습니다. 필요한 데이터를 찾을 수 없습니다.",
                max_retries,
            )

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
                    task_id,
                ): symptom_item.get("failure", f"Item-{i}")
                for i, symptom_item in enumerate(data)
            }

            for future in concurrent.futures.as_completed(future_to_symptom):
                failure = future_to_symptom[future]
                try:
                    result = future.result()

                    publish_rag_completed_event(
                        task_id=task_id,
                        result=result,
                        serial_number=serial_number,
                        customer_id=customer_id,
                        counseling_date=counseling_date,
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


def publish_rag_completed_event(
    task_id: str, result, serial_number: str, customer_id: str, counseling_date: str
) -> None:
    """
    RAG 분석 완료 이벤트를 Kafka에 발행합니다.

    Args:
        task_id: 분석 ID
        result: GPT 응답 결과
        serial_number: 제품 시리얼 넘버
        customer_id: 고객 아이디
        counseling_date: 상담 일자자
    """
    try:
        print("publish_rag_completed_event")

        # DiagnosticResult 객체를 딕셔너리로 변환
        if "solutions" in result and isinstance(result["solutions"], list):
            result["solutions"] = [
                item.to_dict() if hasattr(item, "to_dict") else item
                for item in result["solutions"]
            ]

        event_data = {
            "taskId": task_id,
            "customer_id": customer_id,
            "counseling_date": counseling_date,
            "result": {"serial_number": serial_number, "data": result},
        }

        producer = get_producer()
        if producer:
            # print("=============이벤트발행==============")
            # pprint.pprint(event_data)
            eda.event_broadcast("rag-result", event_data)
            logger.info("RAG 분석 완료 이벤트가 성공적으로 발행되었습니다.")
        else:
            logger.error("Kafka 프로듀서가 설정되지 않았습니다.")
    except Exception as e:  # pylint: disable=broad-except
        logger.error("이벤트 발행 중 오류 발생: %s", e)
