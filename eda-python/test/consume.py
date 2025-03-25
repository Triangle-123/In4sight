"""
Consumer를 통한 Event 수신 테스트 코드
"""

import time
from typing import Any

import eda

eda.create_consumer(bootstrap_servers="localhost:9092", group_id="test")


def callback(message: Any) -> None:
    """
    Event 수신 콜백 함수
    이벤트에서 timestamp 필드를 출력합니다.
    """
    print(message)
    raise Exception("test")  # pylint: disable=broad-exception-raised


eda.event_subscribe("test", "test", callback)

while True:
    time.sleep(1)
