"""
Producer를 통한 Event 전송 테스트 코드
"""

from datetime import datetime

import eda

producer = eda.create_producer(bootstrap_servers="localhost:9092")

eda.event_broadcast(
    "test",
    {
        "message": "Hello, World!",
        "timestamp": datetime.now().isoformat(),
        "data": {"name": "John Doe", "age": 30},
    },
)
