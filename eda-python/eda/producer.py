"""
in4sight 패키지의 producer 모듈
"""

from json import dumps
from typing import Any, Callable, Optional

from kafka import KafkaProducer

_producer: KafkaProducer | None = None


def create_producer(
    bootstrap_servers: str,
    compression_type: str = "gzip",
    value_serializer: Optional[Callable] = lambda x: dumps(x).encode("utf-8"),
) -> KafkaProducer:
    """
    Kafka Producer를 생성합니다.

    Args:
        bootstrap_servers: Kafka 서버 주소
        compression_type: 압축 타입 (기본값: "gzip")
        value_serializer: 값 직렬화 함수 (기본값: JSON 직렬화)

    Returns:
        KafkaProducer 인스턴스
    """

    kafka_producer = KafkaProducer(
        compression_type=compression_type,
        bootstrap_servers=bootstrap_servers,
        value_serializer=value_serializer,
    )
    set_producer(kafka_producer)
    return kafka_producer


def get_producer() -> KafkaProducer | None:
    """
    현재 설정된 producer를 반환합니다.

    Returns:
        현재 설정된 KafkaProducer 인스턴스 또는 None
    """
    return _producer


def set_producer(new_producer: KafkaProducer) -> None:
    """
    모듈 레벨의 producer를 설정합니다.

    Args:
        new_producer: 설정할 KafkaProducer 인스턴스
    """
    # pylint: disable=global-statement
    global _producer
    _producer = new_producer


def event_broadcast(topic: str, message: Any) -> None:
    """
    이벤트를 브로드캐스트합니다.

    Args:
        topic: 메시지를 보낼 Kafka 토픽
        message: 브로드캐스트할 메시지

    Raises:
        RuntimeError: producer가 초기화되지 않은 경우
    """
    producer = get_producer()
    if producer is None:
        raise RuntimeError(
            "Producer가 초기화되지 않았습니다. get_producer_from_settings를 먼저 호출하세요."
        )

    producer.send(topic, message)
    producer.flush()
