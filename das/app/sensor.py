"""
이 모듈은 influxDB에서 sensor data를 가져오고 이상치를 감지합니다
"""

import json

from influxdb_client import InfluxDBClient

from app.config import (INFLUXDB_BUCKET_EVENT, INFLUXDB_BUCKET_SENSOR,
                        INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL)

# influxdb 연결
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

# influxdb에 flux 쿼리 사용
query_api = client.query_api()


def get_refrigerator_sensors_data(serial_number):
    """
    influxDB에서 모든 냉장고 시계열 데이터 가져오는 함수  (냉장실 + 냉동실)
    """

    # 전체 문제 상황을 담을 프롬포트
    anomaly_prompts = []

    # 문제 상황 관련 센서
    related_sensor = []

    result = {}

    # (현재 기준 3시간 전 데이터 ~ 지금까지 데이터)
    sensors_query = f"""
    from(bucket: "{INFLUXDB_BUCKET_SENSOR}")
    |> range(start: -3h)
    |> filter(fn: (r) => r._measurement == "refrigerator" and r.serial_number == "{serial_number}")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> yield()
    """

    event_query = f"""
    from(bucket: "{INFLUXDB_BUCKET_EVENT}")
    |> range(start: -3h)
    |> filter(fn: (r) => r._measurement == "refrigerator" and r.serial_number == "{serial_number}")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> yield()
    """

    # 쿼리 실행 후 pandas DataFrame으로 변환
    df_sensor = query_api.query_data_frame(org=INFLUXDB_ORG, query=sensors_query)
    df_event = query_api.query_data_frame(org=INFLUXDB_ORG, query=event_query)

    # 온도 관련 이상치 감지
    temp_anomalies, temp_sensors = detect_temperature_anomalies(df_sensor, df_event)
    anomaly_prompts.extend(temp_anomalies)
    related_sensor.extend(temp_sensors)

    result["anomaly_prompts"] = anomaly_prompts

    result["product_type"] = "냉장고"

    result["related_sensor"] = related_sensor

    formatted_json = json.dumps(
        result,
        indent=4,  # 4칸 들여쓰기기
        sort_keys=True,
        ensure_ascii=False,  # 한글 그대로 출력
    )

    print(formatted_json)

    return formatted_json


def detect_temperature_anomalies(df, df_event):
    """
    온도 관련 이상 감지 로직
    """
    anomaly_prompts = []
    related_sensor = ["온도"]

    # 내부 온도 이상치 감지
    if "location" in df.columns and "temp_internal" in df.columns:

        # 냉장실 데이터만 가져오기
        fridge_data = df[df["location"] == "fridge"]

        # 냉장실 내부 온도 이상치 감지
        fridge_anomaly_temp_internal = fridge_data[fridge_data["temp_internal"] > 10]

        if not fridge_anomaly_temp_internal.empty:
            anomaly_prompts.append("내부 온도(냉장실) 이상 고온 감지")

        # 냉동실 데이터만 가져오기
        freezer_data = df[df["location"] == "freezer"]

        # 냉동실 내부 온도 이상치 감지
        freezer_anomaly_temp_internal = freezer_data[
            freezer_data["temp_internal"] > -17
        ]

        if not freezer_anomaly_temp_internal.empty:
            anomaly_prompts.append("내부 온도(냉동실) 이상 고온 감지")

        row_anomaly_temp_external = df[df["temp_external"] < 5]
        high_anomaly_temp_external = df[df["temp_external"] > 45]

        if not row_anomaly_temp_external.empty:
            anomaly_prompts.append("외부 온도 이상 저온 감지")

        if not high_anomaly_temp_external.empty:
            anomaly_prompts.append("외부 온도 이상 고온 감지")

    if "event_type" in df_event.columns:

        # 문 열림 이벤트
        door_open_data = df_event[df_event["event_type"] == "door_open"]

        if not door_open_data.empty:

            # 가장 최근 문이 열린 시간
            last_door_open_time = door_open_data["_time"].max()

            # 지금 문이 열려있는 상태인지 판단
            door_close_data = df_event[
                (df_event["event_type"] == "door_close")
                & (df_event["_time"] > last_door_open_time)
            ]

            if door_close_data.empty:
                anomaly_prompts.append("문이 열려있습니다.")

    return anomaly_prompts, related_sensor


get_refrigerator_sensors_data(1234)
