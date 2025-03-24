"""
FastAPI 서버가 켜짐과 동시에 Kafka 연결을 하는 코드입니다.
"""

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

import eda

from app.config import KAFKA_URL
from app.sensor import get_refrigerator_analyze


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI의 lifecycle에서 원하는 행동을 지정하는 함수
    Java Spring에서 kafka-config 같은 느낌
    """
    producer = eda.create_producer(bootstrap_servers=KAFKA_URL)
    consumer = eda.create_consumer(bootstrap_servers=KAFKA_URL, group_id="test-group")
    eda.event_subscribe("test-group", "counseling_request", callback)

    app.state.producer = producer
    app.state.consumer = consumer

    yield

    producer.close()
    consumer.close()


def callback(message: Any) -> None:
    """
    Event 수신 콜백 함수
    """
    print(message)
    for number in message["serialNumbers"]:
        get_refrigerator_analyze(message["taskId"], number, "2024-03-01", "2024-03-02")
