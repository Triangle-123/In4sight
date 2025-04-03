"""
이 모듈은 데이터 분석과 이상치 감지 하고 eda로 다른 서버의 분석 결과를 보내는 모듈입니다.
"""

from influxdb_client import InfluxDBClient

import pandas as pd

from app.api_ref_data_sending import get_ref_refine_data, event_summary
from app.api_wm_data_sending import get_wm_refine_data
from app.api_ac_data_sending import get_ac_refine_data
from app.config import (
    INFLUXDB_BUCKET_EVENT,
    INFLUXDB_BUCKET_SENSOR,
    INFLUXDB_ORG,
    INFLUXDB_TOKEN,
    INFLUXDB_URL,
)
from app.rag_data_sending import broadcast_rag_message
from app.refrigerator_comp_pressure import detect_pressure_anomalies
from app.refrigerator_door import check_door_anormality
from app.refrigerator_fan import check_fan_rpm_anormality
from app.refrigerator_heater import detect_heater_anomalies
from app.refrigerator_load import check_loading_rate_anormality
from app.refrigerator_temp import detect_temperature_anomalies
from app.util import (
    broadcast_event_message,
    broadcast_sensor_message,
    convert_to_iso_utc,
)

LIMIT_OPEN_NUMBER = 50
LIMIT_MAX_INTERVAL = 20 * 60 * 10**9  # 20분을 나노초로 환산

EVENT_DATA_LIST = ["door_open", "door_close"]

# influxdb 연결
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = client.query_api()


def get_analyze(task_id, serial_number, startday, endday):
    """
    시리얼 넘버에 따라 기기 종류를 분류하고 그에 맞춰서 이상치를 판단하도록 하는 함수입니다.
    """

    # 날짜를 RFC3339(ISO) 형식으로 변환
    startday = convert_to_iso_utc(startday)
    endday = convert_to_iso_utc(endday)

    # 센서 데이터 쿼리
    sensors_query = f"""
    from(bucket: "{INFLUXDB_BUCKET_SENSOR}")
    |> range(start: time(v: "{startday}"), stop: time(v: "{endday}"))
    |> filter(fn: (r) => r.serial_number == "{serial_number}")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> yield()
    """

    # 쿼리 실행 후 pandas DataFrame으로 변환
    df_sensor = query_api.query_data_frame(org=INFLUXDB_ORG, query=sensors_query)

    if isinstance(df_sensor, list):
        measurement = df_sensor[0]["_measurement"].iloc[0]
        df_sensor = pd.concat(df_sensor, ignore_index=True)

    else:
        measurement = df_sensor["_measurement"].iloc[0]

    if measurement == "refrigerator":
        event_query = f"""
        from(bucket: "{INFLUXDB_BUCKET_EVENT}")
        |> range(start: time(v: "{startday}"), stop: time(v: "{endday}"))
        |> filter(fn: (r) => r.serial_number == "{serial_number}")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> yield()
        """

        df_event = query_api.query_data_frame(org=INFLUXDB_ORG, query=event_query)

        find_refrigerator_anomality(task_id, serial_number, df_sensor, df_event)

    elif measurement == "washing_machine":
        broadcast_sensor_message(
            task_id,
            serial_number,
            "data_sensor",
            get_wm_refine_data(df_sensor),
        )

    elif measurement == "air_conditioner":
        broadcast_sensor_message(
            task_id,
            serial_number,
            "data_sensor",
            get_ac_refine_data(df_sensor),
        )


def find_refrigerator_anomality(task_id, serial_number, df_sensor, df_event):
    """
    이 함수는 냉장고 센서 데이터를 분석하고 결과를 eda 통신으로 보내는 역할을 합니다.
    """
    anomaly_prompts = []
    related_sensor = []
    anomaly_sensor = []

    # 온도 관련 이상치 감지 (sensor_cols에 센서 컬럼명이 append됨)
    detect_temperature_anomalies(
        df_sensor, df_event, anomaly_prompts, related_sensor, anomaly_sensor
    )

    # 도어 센서 이상치 감지
    check_door_anormality(df_event, anomaly_prompts, related_sensor)

    # 적재량 이상치 감지
    check_loading_rate_anormality(
        df_sensor, anomaly_prompts, related_sensor, anomaly_sensor
    )

    # 히터 이상치 감지
    detect_heater_anomalies(df_sensor, anomaly_prompts, related_sensor, anomaly_sensor)

    check_fan_rpm_anormality(df_sensor, anomaly_prompts, related_sensor, anomaly_sensor)

    # 컴프레서 압력 이상치 감지
    detect_pressure_anomalies(
        df_sensor.copy(), anomaly_prompts, related_sensor, anomaly_sensor
    )

    event_data = event_summary(df_event, df_sensor)

    broadcast_sensor_message(
        task_id,
        serial_number,
        "data_sensor",
        get_ref_refine_data(df_sensor, list(set(anomaly_sensor))),
    )
    broadcast_event_message(task_id, serial_number, "data_event", event_data)

    broadcast_rag_message(task_id, serial_number, "das_result", anomaly_prompts)
