"""
in4sight-eda 패키지의 consumer 모듈
"""

import threading
from json import loads
from typing import Callable, Optional

from kafka import KafkaConsumer

_consumer: dict[str, KafkaConsumer] = {}


def create_consumer(
    bootstrap_servers: str,
    group_id: str,
    enable_auto_commit: bool = True,
    value_deserializer: Optional[Callable] = lambda x: loads(x.decode("utf-8")),
) -> KafkaConsumer:
    """
    Kafka Consumer를 생성합니다.

    Args:
        bootstrap_servers: Kafka 서버 주소
        group_id: 컨슈머 그룹 ID
        auto_offset_reset: 오프셋 재설정 정책 (기본값: "earliest")
        enable_auto_commit: 자동 커밋 여부 (기본값: True)
        value_deserializer: 값 역직렬화 함수 (기본값: JSON 역직렬화)

    Returns:
        KafkaConsumer 인스턴스
    """

    kafka_consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        enable_auto_commit=enable_auto_commit,
        value_deserializer=value_deserializer,
    )
    set_consumer(kafka_consumer, group_id)
    return kafka_consumer


def get_consumer(group_id: str) -> KafkaConsumer | None:
    """
    현재 설정된 consumer를 반환합니다.

    Returns:
        KafkaConsumer 인스턴스 또는 None
    """
    return _consumer.get(group_id)


def set_consumer(new_consumer: KafkaConsumer, group_id: str) -> None:
    """
    모듈 레벨의 consumer를 설정합니다.

    Args:
        new_consumer: 새로운 KafkaConsumer 인스턴스
    """
    _consumer[group_id] = new_consumer


def event_subscribe(group_id: str, topic: str, callback: Callable) -> None:
    """
    특정 토픽에 대한 이벤트 구독을 시작합니다.

    Args:
        topic: 구독할 토픽 이름
        callback: 이벤트 처리 콜백 함수
    """

    def consume_messages():
        """
        메시지 소비 스레드
        """
        consumer = get_consumer(group_id)
        if consumer is None:
            raise ValueError("Consumer가 설정되지 않았습니다.")

        consumer.subscribe([topic])

        for message in consumer:
            callback(message.value)

    consumer_thread = threading.Thread(target=consume_messages, daemon=True)
    consumer_thread.start()
