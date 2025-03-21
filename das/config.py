"""
이 모듈은 환경 변수를 로드하고, InfluxDB 연결 설정을 관리합니다.
"""

import os

from dotenv import load_dotenv

load_dotenv(override=True)

# 환경 변수 설정
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "your-token-here")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my-org")
INFLUXDB_BUCKET_SENSOR = os.getenv("INFLUXDB_BUCKET_SENSOR", "sensor_data")
INFLUXDB_BUCKET_EVENT = os.getenv("INFLUXDB_BUCKET_EVENT", "event_data")
KAFKA_URL = os.getenv("KAFKA_URL", "http://localhost:9092")
