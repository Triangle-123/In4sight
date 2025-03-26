"""
냉장고 온도 이상치를 판단하는 모듈입니다.
"""

from datetime import timedelta

import pandas as pd

from app.util import get_door_times


def is_door_open(time, open_times, close_times):
    """
    주어진 시간(time)이 open_time부터 (close_time + 1시간) 사이에 있는지 판단합니다.
    """
    for ot, ct in zip(open_times, close_times):
        if ot <= time < ct + timedelta(hours=1):
            return True
    return False


def detect_temperature_anomalies(df_sensor, df_event, anomaly_prompts, related_sensor):
    """
    온도 관련 이상 감지 로직입니다.
    """
    open_times_fridge, close_times_fridge = get_door_times(df_event, "fridge")
    open_times_freezer, close_times_freezer = get_door_times(df_event, "freezer")

    def is_door_open_fridge(time):
        return is_door_open(time, open_times_fridge, close_times_fridge)

    def is_door_open_freezer(time):
        return is_door_open(time, open_times_freezer, close_times_freezer)

    if "location" in df_sensor.columns and "temp_internal" in df_sensor.columns:
        process_fridge_temperature(
            df_sensor, is_door_open_fridge, anomaly_prompts, related_sensor
        )
        process_freezer_temperature(
            df_sensor,
            is_door_open_freezer,
            anomaly_prompts,
            related_sensor,
        )

    if "temp_external" in df_sensor.columns:
        process_external_temperature(df_sensor, anomaly_prompts, related_sensor)


def process_fridge_temperature(
    df_sensor, is_door_open_fridge, anomaly_prompts, related_sensor
):
    """
    냉장실 온도 이상을 감지하는 함수입니다.
    """
    fridge_data = df_sensor[df_sensor["location"] == "fridge"]
    valid_fridge_df = filter_valid_temperature_data(fridge_data, is_door_open_fridge)

    if not valid_fridge_df.empty:
        fridge_anomaly = valid_fridge_df[valid_fridge_df["temp_internal"] >= 10]
        if not fridge_anomaly.empty:
            record_anomaly(5, anomaly_prompts, related_sensor)

        if not fridge_data[fridge_data["temp_internal"] >= 20].empty:
            record_anomaly(6, anomaly_prompts, related_sensor)


def process_freezer_temperature(
    df_sensor, is_door_open_freezer, anomaly_prompts, related_sensor
):
    """
    냉동실 온도 이상을 감지하는 함수입니다.
    """
    freezer_data = df_sensor[df_sensor["location"] == "freezer"]
    valid_freezer_df = filter_valid_temperature_data(freezer_data, is_door_open_freezer)

    if not valid_freezer_df.empty:
        freezer_anomaly = valid_freezer_df[valid_freezer_df["temp_internal"] >= -17]
        if not freezer_anomaly.empty:
            record_anomaly(7, anomaly_prompts, related_sensor)


def process_external_temperature(df_sensor, anomaly_prompts, related_sensor):
    """
    냉장고 외부 온도 이상을 감지하는 함수입니다.
    """
    low_external = df_sensor[df_sensor["temp_external"] < 5]
    high_external = df_sensor[df_sensor["temp_external"] > 45]

    if not low_external.empty:
        record_anomaly(8, anomaly_prompts, related_sensor)
    if not high_external.empty:
        record_anomaly(9, anomaly_prompts, related_sensor)


def filter_valid_temperature_data(sensor_data, is_door_open_fun):
    """
    전체 데이터 중에서 _time 컬럼만 추출하는 함수입니다.
    """
    valid_rows = [
        row for _, row in sensor_data.iterrows() if not is_door_open_fun(row["_time"])
    ]
    return pd.DataFrame(valid_rows, columns=sensor_data.columns)


def record_anomaly(message, anomaly_prompts, related_sensor):
    """
    감지한 이상치를 저장하는 함수입니다.
    """
    anomaly_prompts.append(message)
    related_sensor.append("온도")
