"""
이 모듈은 데이터 분석과 이상치 감지 하고 eda로 다른 서버의 분석 결과를 보내는 모듈입니다.
"""

import time as t
from datetime import timedelta
from json import dumps
from typing import Any

import eda
import pandas as pd
from influxdb_client import InfluxDBClient

from .config import (INFLUXDB_BUCKET_EVENT, INFLUXDB_BUCKET_SENSOR,
                     INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL, KAFKA_URL)
from .util import convert_to_iso_utc

eda.create_producer(bootstrap_servers=KAFKA_URL)
eda.create_consumer(bootstrap_servers=KAFKA_URL, group_id="test-group")


def callback(message: Any) -> None:
    """
    Event 수신 콜백 함수
    """
    print(message)
    for number in message:
        get_refrigerator_analyze(number, "2024-03-01", "2024-03-02")


print("Subscribing to test event")
eda.event_subscribe("test-group", "counseling_request", callback)
print("Subscribed to test event")


LIMIT_OPEN_NUMBER = 50
LIMIT_MAX_INTERVAL = 20 * 60 * 10**9  # 20분을 나노초로 환산

# influxdb 연결
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = client.query_api()


def get_door_times(df_event, location):
    """
    지정한 location에 해당하는 문 이벤트의 open/close 시간 리스트를 반환합니다.
    """
    df_loc = df_event[df_event["location"] == location]
    open_times = list(df_loc[df_loc["event_type"] == "door_open"]["_time"])
    close_times = list(df_loc[df_loc["event_type"] == "door_close"]["_time"])
    return open_times, close_times


def is_door_open(time, open_times, close_times):
    """
    주어진 시간(time)이 open_time부터 (close_time + 1시간) 사이에 있는지 판단합니다.
    """
    for ot, ct in zip(open_times, close_times):
        if ot <= time < ct + timedelta(hours=1):
            return True
    return False


def detect_temperature_anomalies(
    df_sensor, df_event, anomaly_prompts, related_sensor, anomaly_sensors
):
    """
    온도 관련 이상 감지 로직
    """
    # 냉장실 문 이벤트 정보
    open_times_fridge, close_times_fridge = get_door_times(df_event, "fridge")

    # 냉동실 문 이벤트 정보
    open_times_freezer, close_times_freezer = get_door_times(df_event, "freezer")

    def is_door_open_fridge(time):
        return is_door_open(time, open_times_fridge, close_times_fridge)

    def is_door_open_freezer(time):
        return is_door_open(time, open_times_freezer, close_times_freezer)

    # location과 temp_internal이 있는 경우만 처리
    if "location" in df_sensor.columns and "temp_internal" in df_sensor.columns:
        # === 냉장실 (fridge) 처리 ===
        fridge_data = df_sensor[df_sensor["location"] == "fridge"]
        valid_fridge_rows = []
        for _, row in fridge_data.iterrows():
            if not is_door_open_fridge(row["_time"]):
                valid_fridge_rows.append(row)

        valid_fridge_df = pd.DataFrame(valid_fridge_rows, columns=fridge_data.columns)

        # 냉장실 내부 온도가 10도 이상이면 이상치
        if not valid_fridge_df.empty:
            fridge_anomaly = valid_fridge_df[valid_fridge_df["temp_internal"] >= 10]
            if not fridge_anomaly.empty:
                anomaly_prompts.append("내부 온도(냉장실) 이상 고온 감지")
                related_sensor.append("온도")
                anomaly_sensors.append("temp_internal")

        # === 냉동실 (freezer) 처리 ===
        freezer_data = df_sensor[df_sensor["location"] == "freezer"]
        valid_freezer_rows = []
        for _, row in freezer_data.iterrows():
            if not is_door_open_freezer(row["_time"]):
                valid_freezer_rows.append(row)

        valid_freezer_df = pd.DataFrame(
            valid_freezer_rows, columns=freezer_data.columns
        )

        # 냉동실 내부 온도가 -17도 이상이면 이상치
        if not valid_freezer_df.empty:
            freezer_anomaly = valid_freezer_df[valid_freezer_df["temp_internal"] >= -17]
            if not freezer_anomaly.empty:
                anomaly_prompts.append("내부 온도(냉동실) 이상 고온 감지")
                related_sensor.append("온도")
                anomaly_sensors.append("temp_internal")

    # === 외부 온도 감지 (문 이벤트 무관) ===
    if "temp_external" in df_sensor.columns:
        low_external = df_sensor[df_sensor["temp_external"] < 5]
        high_external = df_sensor[df_sensor["temp_external"] > 45]
        if not low_external.empty:
            anomaly_prompts.append("외부 온도 이상 저온 감지")
            related_sensor.append("온도")
            anomaly_sensors.append("temp_external")
        if not high_external.empty:
            anomaly_prompts.append("외부 온도 이상 고온 감지")
            related_sensor.append("온도")
            anomaly_sensors.append("temp_external")


def check_door_anormality(df_event, anormality_list, related_sensor):
    """
    냉장실, 냉동실의 도어 센서 이상치를 판단하는 로직입니다.
    """
    # 냉장실 문 이벤트
    open_times_fridge, close_times_fridge = get_door_times(df_event, "fridge")

    # 냉동실 문 이벤트
    open_times_freezer, close_times_freezer = get_door_times(df_event, "freezer")

    def check_location_door(location_name, open_times, close_times):
        open_number = len(open_times)
        max_interval = 0
        for ot, ct in zip(open_times, close_times):
            interval = int((ct - ot).value)  # ns 단위
            max_interval = max(max_interval, interval)

        # 문 열림 횟수 이상
        if open_number >= LIMIT_OPEN_NUMBER:
            anormality_list.append(f"{location_name} 문 열림 횟수가 너무 많음")
            related_sensor.append("문")

        # 문이 너무 오래 열려 있거나 닫히지 않은 경우
        if max_interval >= LIMIT_MAX_INTERVAL:
            anormality_list.append(
                f"{location_name} 문이 너무 오래 열려 있었거나 문이 잘 닫히지 않았음"
            )
            related_sensor.append("문")

    # 냉장실과 냉동실 각각 검사
    check_location_door("냉장실", open_times_fridge, close_times_fridge)
    check_location_door("냉동실", open_times_freezer, close_times_freezer)


def get_refrigerator_analyze(serial_number, startday, endday):
    """
    이 함수는 냉장고 센서 데이터를 분석하고 결과를 eda 통신으로 보내는 역할을 합니다
    """

    anomaly_prompts = []
    related_sensor = []
    default_cols = ["_time", "location"]
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

    # sensor_cols가 비어있는지 리스트의 길이로 체크
    if sensor_cols:
        anomaly_sensors = sensor_cols + default_cols

        # anomaly_sensors에 포함된 컬럼 선택 및 정렬
        sensor = df_sensor[list(set(anomaly_sensors))].sort_values(["_time"])

        # wide format -> long format 변환: _time, location은 id_vars, 나머지 센서 컬럼은 value_vars로 처리
        sensor_long = sensor.melt(
            id_vars=["_time", "location"], var_name="sensor", value_name="value"
        ).rename(columns={"_time": "time"})

        # value가 null인 행 제거
        sensor_long = sensor_long.dropna(subset=["value"])

        # JSON 변환 (pretty-print)
        request_sensor = sensor_long.to_json(
            orient="records", date_format="iso", date_unit="s", indent=4
        )

        print(request_sensor)

        event = (
            df_event[["_time", "event_type", "location"]]
            .sort_values("_time")
            .rename(columns={"_time": "time"})
        )

        request_event = event.to_json(
            orient="records", date_format="iso", date_unit="s", indent=4
        )

        eda.event_broadcast("data_sensor", request_sensor)
        eda.event_broadcast("data_event", request_event)
    else:
        eda.event_broadcast("data_sensor", "정상")

    result["anomaly_prompts"] = anomaly_prompts
    result["product_type"] = "냉장고"
    result["related_sensor"] = list(set(related_sensor))

    formatted_json = dumps(result, indent=4, sort_keys=True, ensure_ascii=False)

    print(formatted_json)


if __name__ == "__main__":
    while True:
        t.sleep(1)
