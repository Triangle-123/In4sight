"""
냉장실의 이상치를 판단하는 로직입니다.
"""

import os
from datetime import timedelta

import influxdb_client

from util import convert_to_iso_utc

token = os.environ.get("INFLUXDB_TOKEN")
ORG = "testinfluxdb"
URL = "http://localhost:8086"
write_client = influxdb_client.InfluxDBClient(url=URL, token=token, org=ORG)
SENSOR_BUCKET = "sensor_data"
EVENT_BUCKET = "event_data"

USER_SETTING_TEMP = 4
LIMIT_OPEN_NUMBER = 50
LIMIT_MAX_INTERVAL = 20 * 60 * 10**9


def get_data_framge(startday, endday, serial_number):
    """
    냉장실의 센서 데이터와 이벤트 데이터를 가져옵니다.
    """
    startday = convert_to_iso_utc(startday)
    endday = convert_to_iso_utc(endday)

    sensor_query = f"""
        from(bucket: "{SENSOR_BUCKET}")
        |> range(start: time(v: "{startday}"), stop: time(v: "{endday}"))
        |> filter(fn: (r) => r.serial_number == "{serial_number}")
        |> filter(fn: (r) => r._measurement == "refrigerator" and r.location == "fridge")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> yield()
        """
    event_query = f"""
        from(bucket: "{EVENT_BUCKET}")
        |> range(start: time(v: "{startday}"), stop: time(v: "{endday}"))
        |> filter(fn: (r) => r.serial_number == "{serial_number}")
        |> filter(fn: (r) => r._measurement == "refrigerator" and r.location == "fridge")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> yield()
        """
    df_sensor = write_client.query_api().query_data_frame(query=sensor_query)
    df_event = write_client.query_api().query_data_frame(query=event_query)
    return df_sensor, df_event


def check_temp_anormality(df_sensor, df_event, anormality_list):
    """
    냉장실의 온도 이상치가 존재하는 지 판단합니다.
    """
    df_open_time = df_event[df_event["event_type"] == "door_open"]
    df_close_time = df_event[df_event["event_type"] == "door_close"]
    open_times = list(df_open_time["_time"])
    close_times = list(df_close_time["_time"])

    cnt = 0

    for _, row in df_sensor.iterrows():
        check = True
        open_times_length = len(open_times)

        for index in range(open_times_length):
            if (
                open_times[index]
                <= row["_time"]
                < close_times[index] + timedelta(hours=1)
            ):
                check = False

        if not check:
            continue

        if row["temp_internal"] >= USER_SETTING_TEMP + 5:
            cnt += 1

    if cnt > 0:
        anormality_list.append("내부 온도(냉장실) 이상 고온 감지")


def check_door_anormality(df_event, anormality_list):
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
    if max_interval >= LIMIT_MAX_INTERVAL:
        anormality_list.append("문이 너무 오래 열려 있었거나 문이 잘 닫히지 않았음")


def analyze(startday, endday, serial_number):
    """
    모듈 외부에서 어느 기기의 이상치를 판단할 지 결정하는 데에 필요한 파라미터를 받아옵니다.
    """

    df_sensor, df_event = get_data_framge(startday, endday, serial_number)
    anormality_list = []

    check_temp_anormality(df_sensor, df_event, anormality_list)
    check_door_anormality(df_event, anormality_list)

    return {"anormality": anormality_list}
