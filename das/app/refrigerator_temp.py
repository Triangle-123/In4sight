"""
냉장고 온도 이상치를 판단하는 모듈입니다.
"""

from datetime import timedelta

import pandas as pd

from app.util import get_door_times, detect_anomalies_range, make_event_set


def is_door_open(time, open_times, close_times):
    """
    주어진 시간(time)이 open_time부터 (close_time + 1시간) 사이에 있는지 판단합니다.
    """
    for ot, ct in zip(open_times, close_times):
        if ot <= time < ct + timedelta(hours=1):
            return True
    return False


def detect_temperature_anomalies(
    df_sensor, df_event, anomaly_prompts, related_sensor, anomaly_sensor
):
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
            df_sensor,
            is_door_open_fridge,
            anomaly_prompts,
            related_sensor,
            anomaly_sensor,
        )
        process_freezer_temperature(
            df_sensor,
            is_door_open_freezer,
            anomaly_prompts,
            related_sensor,
            anomaly_sensor,
        )

    if "temp_external" in df_sensor.columns:
        process_external_temperature(
            df_sensor, anomaly_prompts, related_sensor, anomaly_sensor
        )


def process_fridge_temperature(
    df_sensor, is_door_open_fridge, anomaly_prompts, related_sensor, anomaly_sensor
):
    """
    냉장실 온도 이상을 감지하는 함수입니다.
    """
    fridge_data = df_sensor[df_sensor["location"] == "fridge"]
    valid_fridge_df = filter_valid_temperature_data(fridge_data, is_door_open_fridge)

    high_temp_fridge_df = detect_anomalies_range(
        valid_fridge_df, "temp_internal", 10, -20
    )
    hot_temp_fridge_df = detect_anomalies_range(fridge_data, "temp_internal", 20, -20)

    if high_temp_fridge_df:
        eventset = make_event_set(high_temp_fridge_df, "냉장실 고내 온도가 높았습니다.")

        if eventset:
            record_anomaly(
                (5, eventset),
                anomaly_prompts,
                related_sensor,
                anomaly_sensor,
                "temp_internal",
            )

    if hot_temp_fridge_df:
        eventset = []

        for start, end in hot_temp_fridge_df:

            start_str = start.strftime("%Y-%m-%d %H:%M:%S")
            end_str = end.strftime("%Y-%m-%d %H:%M:%S")
            eventset.append(
                f"{start_str} ~ {end_str} 구간에서 뜨거운 음식을 넣었을 가능성이 있습니다."
            )

        record_anomaly(
            (6, eventset),
            anomaly_prompts,
            related_sensor,
            anomaly_sensor,
            "temp_internal",
        )


def process_freezer_temperature(
    df_sensor, is_door_open_freezer, anomaly_prompts, related_sensor, anomaly_sensor
):
    """
    냉동실 온도 이상을 감지하는 함수입니다.
    """
    freezer_data = df_sensor[df_sensor["location"] == "freezer"]
    valid_freezer_df = filter_valid_temperature_data(freezer_data, is_door_open_freezer)

    high_temp_freezer_df = detect_anomalies_range(
        valid_freezer_df, "temp_internal", -17, -100
    )
    if high_temp_freezer_df:
        eventset = make_event_set(
            high_temp_freezer_df, "냉동실 고내 온도가 높았습니다."
        )

        if eventset:
            record_anomaly(
                (7, eventset),
                anomaly_prompts,
                related_sensor,
                anomaly_sensor,
                "temp_internal",
            )


def process_external_temperature(
    df_sensor, anomaly_prompts, related_sensor, anomaly_sensor
):
    """
    냉장고 외부 온도 이상을 감지하는 함수입니다.
    """
    if not df_sensor[df_sensor["temp_external"] < 5].empty:
        record_anomaly(
            8, anomaly_prompts, related_sensor, anomaly_sensor, "temp_external"
        )
    if not df_sensor[df_sensor["temp_external"] > 45].empty:
        record_anomaly(
            9, anomaly_prompts, related_sensor, anomaly_sensor, "temp_external"
        )


def filter_valid_temperature_data(sensor_data, is_door_open_fun):
    """
    전체 데이터 중에서 _time 컬럼만 추출하는 함수입니다.
    """
    valid_rows = [
        row for _, row in sensor_data.iterrows() if not is_door_open_fun(row["_time"])
    ]
    return pd.DataFrame(valid_rows, columns=sensor_data.columns)


def record_anomaly(
    message, anomaly_prompts, related_sensor, anomaly_sensor, sensor_column
):
    """
    감지한 이상치를 저장하는 함수입니다.
    """
    anomaly_prompts.append(message)
    related_sensor.append("온도")
    anomaly_sensor.append(sensor_column)
