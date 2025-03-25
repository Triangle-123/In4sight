"""
컴프레서 압력 이상치 테스트 코드입니다.
"""

from influxdb_client import InfluxDBClient

from app.comp_pressure import detect_pressure_anomalies
from app.config import INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL

client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG,
)
query_api = client.query_api()

NORMAL_SENSORS_QUERY = """
from(bucket: "test_data")
|> range(start: time(v: "2024-03-01T00:00:00+09:00"), stop: time(v: "2024-03-03T00:00:00+09:00"))
|> filter(fn: (r) => r._measurement == "refrigerator" and r.serial_number == "test_016")
|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
|> yield()
"""

ERROR_SENSORS_QUERY = """
from(bucket: "test_data")
|> range(start: time(v: "2024-03-01T00:00:00+09:00"), stop: time(v: "2024-03-03T00:00:00+09:00"))
|> filter(fn: (r) => r._measurement == "refrigerator" and r.serial_number == "test_017")
|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
|> yield()
"""

WINDOW_LENGTH = 14
POLYORDER = 1

df_normal_sensor = query_api.query_data_frame(
    org=INFLUXDB_ORG, query=NORMAL_SENSORS_QUERY
)

anormality_list1 = []
related_sensor1 = []

detect_pressure_anomalies(df_normal_sensor, anormality_list1, related_sensor1)

assert not anormality_list1
assert not related_sensor1


df_error_sensor = query_api.query_data_frame(
    org=INFLUXDB_ORG, query=ERROR_SENSORS_QUERY
)

anormality_list2 = []
related_sensor2 = []

detect_pressure_anomalies(df_error_sensor, anormality_list2, related_sensor2)

assert anormality_list2[0].startswith("[컴프레서 압력 이상치 범위]")
assert related_sensor2 == ["컴프레서 압력"]
