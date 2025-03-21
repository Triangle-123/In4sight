"""
이 모듈은 데이터 분석과 이상치 감지 하고 eda로 다른 서버의 분석 결과를 보내는 모듈입니다.
"""

from json import dumps

import eda
import pandas as pd
from influxdb_client import InfluxDBClient

from .config import (
    INFLUXDB_BUCKET_EVENT,
    INFLUXDB_BUCKET_SENSOR,
    INFLUXDB_ORG,
    INFLUXDB_TOKEN,
    INFLUXDB_URL,
)
from .util import convert_to_iso_utc

from .refrigerator_door import check_door_anormality
from .refrigerator_temp import detect_temperature_anomalies

LIMIT_OPEN_NUMBER = 50
LIMIT_MAX_INTERVAL = 20 * 60 * 10**9  # 20분을 나노초로 환산

SENSOR_DATA_LIST = [
    "temp_internal",
    "temp_external",
    "_time",
    "location",
    "serial_number",
]
DEFAULT_DATA_LIST = ["_time", "location", "serial_number"]

# influxdb 연결
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = client.query_api()


def get_refrigerator_analyze(serial_number, startday, endday):
    """
    이 함수는 냉장고 센서 데이터를 분석하고 결과를 eda 통신으로 보내는 역할을 합니다
    """

    anomaly_prompts = []
    related_sensor = []
    sensor_cols = []  # 온도 이상 감지 시 여기에 센서 컬럼명이 append 됨.
    result = {}

    # 날짜를 RFC3339(ISO) 형식으로 변환
    startday = convert_to_iso_utc(startday)
    endday = convert_to_iso_utc(endday)

    # 센서 데이터 쿼리
    sensors_query = f"""
    from(bucket: "{INFLUXDB_BUCKET_SENSOR}")
    |> range(start: time(v: "{startday}"), stop: time(v: "{endday}"))
    |> filter(fn: (r) => r._measurement == "refrigerator" and r.serial_number == "{serial_number}")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> yield()
    """

    # 이벤트 데이터 쿼리
    event_query = f"""
    from(bucket: "{INFLUXDB_BUCKET_EVENT}")
    |> range(start: time(v: "{startday}"), stop: time(v: "{endday}"))
    |> filter(fn: (r) => r._measurement == "refrigerator" and r.serial_number == "{serial_number}")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> yield()
    """

    # 쿼리 실행 후 pandas DataFrame으로 변환
    df_sensor = query_api.query_data_frame(org=INFLUXDB_ORG, query=sensors_query)
    df_event = query_api.query_data_frame(org=INFLUXDB_ORG, query=event_query)

    if isinstance(df_sensor, list):
        df_sensor = pd.concat(df_sensor)

    # 온도 관련 이상치 감지 (sensor_cols에 센서 컬럼명이 append됨)
    detect_temperature_anomalies(
        df_sensor, df_event, anomaly_prompts, related_sensor, sensor_cols
    )

    # 도어 센서 이상치 감지
    check_door_anormality(df_event, anomaly_prompts, related_sensor)

    # anomaly_sensors에 포함된 컬럼 선택 및 정렬
    sensor = df_sensor[SENSOR_DATA_LIST].sort_values(["_time"])

    # wide format -> long format 변환: _time, location은 id_vars, 나머지 센서 컬럼은 value_vars로 처리
    sensor = sensor.melt(
        id_vars=DEFAULT_DATA_LIST, var_name="sensor", value_name="value"
    ).rename(columns={"_time": "time"})

    # value가 null인 행 제거
    sensor = sensor.dropna(subset=["value"])

    # JSON 변환 (pretty-print)
    sensor = sensor.to_json(
        orient="records", date_format="iso", date_unit="s", indent=4
    )

    print(sensor)

    event = (
        df_event[["_time", "event_type", "location"]]
        .sort_values("_time")
        .rename(columns={"_time": "time"})
    )

    event = event.to_json(orient="records", date_format="iso", date_unit="s", indent=4)

    eda.event_broadcast("data_sensor", sensor)
    eda.event_broadcast("data_event", event)

    result["anomaly_prompts"] = anomaly_prompts
    result["product_type"] = "냉장고"
    result["related_sensor"] = list(set(related_sensor))

    formatted_json = dumps(result, indent=4, sort_keys=True, ensure_ascii=False)

    print(formatted_json)

    eda.event_broadcast("das_result", formatted_json)
