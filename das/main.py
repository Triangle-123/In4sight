"""
Integration Test
Producer와 Consumer를 통한 통합 테스트
"""

import time
from typing import Any

import eda

eda.create_producer(bootstrap_servers="j12s004.p.ssafy.io:8003")
eda.create_consumer(bootstrap_servers="j12s004.p.ssafy.io:8003", group_id="test-group")

MESSAGE = None


def callback(message: Any) -> None:
    """
    Event 수신 콜백 함수
    """
    # pylint: disable=global-statement
    global MESSAGE
    print("success")
    print("message : " + message)
    message = "Hello, World!"
    MESSAGE = message


print("Subscribing to test event")
eda.event_subscribe("test-group", "java", callback)
print("Subscribed to test event")

eda.event_broadcast("python", "Hello, World!")

TIME_LIMIT = 1000
while TIME_LIMIT > 0:
    if MESSAGE is not None:
        break
    TIME_LIMIT -= 1
    time.sleep(1)

assert MESSAGE == "Hello, World!"
