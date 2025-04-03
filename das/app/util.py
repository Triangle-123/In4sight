"""
다수의 모듈에서 사용하는 함수들을 모아놓은 곳입니다.
"""

import logging
from datetime import datetime, timedelta

import eda


def convert_to_iso_utc(date_str):
    """
    다양한 시간 입력 포맷을 일관되게 처리해줍니다.
    """
    # 지원하는 입력 포맷
    formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue
    else:
        print("Error converting date: Invalid date format")
        return None

    # UTC 기준 ISO 8601 포맷으로 변환
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def get_door_times(df_event, location):
    """
    지정한 location에 해당하는 문 이벤트의 open/close 시간 리스트를 반환합니다.
    """

    if "location" not in df_event.columns:
        logging.warning("[get_door_times] 'location' 컬럼이 존재하지 않습니다.")
        return [], []

    df_loc = df_event[df_event["location"] == location]

    if df_loc.empty:
        logging.warning(
            "[get_door_times] '%s' 위치의 이벤트 데이터가 없습니다.", location
        )
        return [], []

    open_times = list(df_loc[df_loc["event_type"] == "door_open"]["_time"])
    close_times = list(df_loc[df_loc["event_type"] == "door_close"]["_time"])

    return open_times, close_times


def broadcast_sensor_message(task_id, serial_number, topic, data):
    """
    eda를 통해 메시지를 broadcast를 해주는 함수입니다.
    """
    message = {}

    message["taskId"] = task_id
    message["serialNumber"] = serial_number
    message["sensor_data"] = data

    eda.event_broadcast(topic, message)


def broadcast_event_message(task_id, serial_number, topic, data):
    """
    eda를 통해 이벤트 데이터 메시지를 broadcast를 해주는 함수입니다.
    """
    message = {}

    message["taskId"] = task_id
    message["serialNumber"] = serial_number
    message["event_data"] = data

    eda.event_broadcast(topic, message)


def detect_anomalies_range(df_sensor, field, max_threshold, min_threshold):
    """
    이상치를 가지는 범위를 판단하는 함수입니다.
    """

    result = []

    if df_sensor[field].max() > max_threshold or df_sensor[field].min() < min_threshold:
        result = []
        countinues = False
        error_duration = {"start": None, "end": None}

        for i in range(len(df_sensor)):
            if (
                df_sensor[field].iloc[i] > max_threshold
                or df_sensor[field].iloc[i] < min_threshold
            ):
                if countinues:
                    error_duration["end"] = df_sensor["_time"].iloc[i]
                else:
                    error_duration["start"] = df_sensor["_time"].iloc[i]
                    error_duration["end"] = df_sensor["_time"].iloc[i]
                    countinues = True
            else:
                if countinues:
                    result.append([error_duration["start"], error_duration["end"]])
                countinues = False

        if countinues:
            result.append([error_duration["start"], df_sensor["_time"].iloc[-1]])

    return result


def make_event_set(anomality_period, suffix_string):
    """
    유효한 이상치 구간을 이벤트 문자열로 변환하는 함수입니다.
    """
    event = []

    for start, end in anomality_period:
        if end - start <= timedelta(minutes=15):
            continue

        start_str = start.strftime("%Y-%m-%d %H:%M:%S")
        end_str = end.strftime("%Y-%m-%d %H:%M:%S")
        event.append(f"{start_str} ~ {end_str} 구간에서 {suffix_string}")

    return event
