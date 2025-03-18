"""
이 모듈은 influxDB에서 sensor data를 가져오고 이상치를 감지합니다
"""

import json
from datetime import timedelta

import pandas as pd
from influxdb_client import InfluxDBClient

from app.config import (INFLUXDB_BUCKET_EVENT, INFLUXDB_BUCKET_SENSOR,
                        INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL)
from util import convert_to_iso_utc

LIMIT_OPEN_NUMBER = 50
LIMIT_MAX_INTERVAL = 20 * 60 * 10**9

# influxdb 연결
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

# influxdb에 flux 쿼리 사용
query_api = client.query_api()


def get_refrigerator_analyze(serial_number, startday, endday):
    """
    influxDB에서 모든 냉장고 시계열 데이터 가져오는 함수  (냉장실 + 냉동실)
    """

    # 전체 문제 상황을 담을 프롬포트
    anomaly_prompts = []

    # 문제 상황 관련 센서
    related_sensor = []

    result = {}

    startday = convert_to_iso_utc(startday)
    endday = convert_to_iso_utc(endday)

    sensors_query = f"""
    from(bucket: "{INFLUXDB_BUCKET_SENSOR}")
    |> range(start: time(v: "{startday}"), stop: time(v: "{endday}"))
    |> filter(fn: (r) => r._measurement == "refrigerator" and r.serial_number == "{serial_number}")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> yield()
    """

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

    # 온도 관련 이상치 감지
    detect_temperature_anomalies(df_sensor, df_event, anomaly_prompts, related_sensor)

    # 도어 센서 이상치 감지지
    check_door_anormality(df_event, anomaly_prompts, related_sensor)

    result["anomaly_prompts"] = anomaly_prompts

    result["product_type"] = "냉장고"

    result["related_sensor"] = list(set(related_sensor))

    formatted_json = json.dumps(
        result,
        indent=4,  # 4칸 들여쓰기기
        sort_keys=True,
        ensure_ascii=False,  # 한글 그대로 출력
    )

    print(formatted_json)

    return formatted_json


def detect_temperature_anomalies(df_sensor, df_event, anomaly_prompts, related_sensor):
    """
    온도 관련 이상 감지 로직
    """
    # 이벤트 데이터에서 문 열림/닫힘 시간 추출
    df_open_time = df_event[df_event["event_type"] == "door_open"]
    df_close_time = df_event[df_event["event_type"] == "door_close"]
    open_times = list(df_open_time["_time"])
    close_times = list(df_close_time["_time"])

    # 주어진 시간이 문 열림 이벤트 구간에 포함되는지 확인
    def is_door_open(time):
        for open_time, close_time in zip(open_times, close_times):
            if open_time <= time < close_time + timedelta(hours=1):
                return True
        return False

    # 온도 관련 컬럼과 location이 존재하는 경우에만 처리
    if "location" in df_sensor.columns and "temp_internal" in df_sensor.columns:

        # === 냉장실 (fridge) 처리 ===
        fridge_data = df_sensor[df_sensor["location"] == "fridge"]
        valid_fridge_rows = []
        for _, row in fridge_data.iterrows():
            if not is_door_open(row["_time"]):
                valid_fridge_rows.append(row)

        valid_fridge_df = pd.DataFrame(valid_fridge_rows)

        # 냉장실 내부 온도가 10도 이상이면 이상치로 판단
        if not valid_fridge_df.empty:
            fridge_anomaly = valid_fridge_df[valid_fridge_df["temp_internal"] >= 10]
            if not fridge_anomaly.empty:
                print("hi")
                anomaly_prompts.append("내부 온도(냉장실) 이상 고온 감지")
                related_sensor.append("온도")

        # === 냉동실 (freezer) 처리 ===
        freezer_data = df_sensor[df_sensor["location"] == "freezer"]
        valid_freezer_rows = []
        for _, row in freezer_data.iterrows():
            if not is_door_open(row["_time"]):
                valid_freezer_rows.append(row)

        valid_freezer_df = pd.DataFrame(valid_freezer_rows)

        # 냉동실 내부 온도가 -17도 이상이면 이상치로 판단
        if not valid_freezer_df.empty:
            freezer_anomaly = valid_freezer_df[valid_freezer_df["temp_internal"] >= -17]
            if not freezer_anomaly.empty:
                anomaly_prompts.append("내부 온도(냉동실) 이상 고온 감지")
                related_sensor.append("온도")

    # === 외부 온도 감지 (문 열림 이벤트 고려 없이 판별) ===
    if "temp_external" in df_sensor.columns:
        low_external = df_sensor[df_sensor["temp_external"] < 5]
        high_external = df_sensor[df_sensor["temp_external"] > 45]
        if not low_external.empty:
            anomaly_prompts.append("외부 온도 이상 저온 감지")
            related_sensor.append("온도")
        if not high_external.empty:
            anomaly_prompts.append("외부 온도 이상 고온 감지")
            related_sensor.append("온도")


def check_door_anormality(df_event, anormality_list, related_sensor):
    """
    냉장실의 도어 센서의 이상치를 판단하는 로직입니다.
    """
    df_open_time = df_event[df_event["event_type"] == "door_open"]
    df_close_time = df_event[df_event["event_type"] == "door_close"]

    open_times = list(df_open_time["_time"])
    close_times = list(df_close_time["_time"])

    open_number = len(open_times)
    max_interval = 0
    open_times_length = len(open_times)

    for index in range(open_times_length):
        max_interval = max(
            max_interval, int((close_times[index] - open_times[index]).value)
        )

    if open_number >= LIMIT_OPEN_NUMBER:
        anormality_list.append("문 열림 횟수가 너무 많음")
        related_sensor.append("문")

    if max_interval >= LIMIT_MAX_INTERVAL:
        anormality_list.append("문이 너무 오래 열려 있었거나 문이 잘 닫히지 않았음")
        related_sensor.append("문")
