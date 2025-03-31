"""
API 서버에 데이터를 보내는 형식으로 바꾸기 위한 모듈입니다.
"""

import pprint
from collections import defaultdict

import pandas as pd

METRICS = {
    "fan_rpm": "팬 속도 변화",
    "heater_temp": "히터 온도 변화",
    "load_percent": "적재량 변화",
    "refrigerant_pressure": "압력 센서 변화",
    "temp_external": "외부 온도 변화",
    "temp_internal": "내부 온도 변화",
    "fridge": "냉장실",
    "freezer": "냉동실",
}


UNIT = {
    "fan_rpm": "rpm",
    "heater_temp": "℃",
    "load_percent": "%",
    "refrigerant_pressure": "kPa",
    "temp_external": "℃",
    "temp_internal": "℃",
}

ICON = {
    "fan_rpm": "Fan",
    "heater_temp": "Heater",
    "load_percent": "Refrigerator",
    "refrigerant_pressure": "CircleGauge",
    "temp_external": "ThermometerSun",
    "temp_internal": "ThermometerSnowflake",
}


def api_data_refine(df, anomaly_sensor=None):
    """
    API 서버 전송용으로 센서 시계열 데이터 + 현재 상태 데이터를 구조화
    """
    dataset = defaultdict(list)
    field_unit_map = {}
    field_icon_map = {}
    field_abnormal_map = {}

    anomaly_sensor = anomaly_sensor or []

    for data in df:
        time_str = data["time"]
        sensor_key = data["sensor"]
        location_key = data.get("location")

        # 기본 센서명 → 한국어 필드명
        base_field_name = METRICS.get(sensor_key)
        unit = UNIT.get(sensor_key)
        icon = ICON.get(sensor_key)

        if location_key:
            prefix = METRICS.get(location_key, "")
            field = f"{prefix} {base_field_name}"
        else:
            field = base_field_name

        value = data["value"]
        if sensor_key == "fan_rpm":
            value = int(value)

        # 시계열 데이터 쌓기
        dataset[field].append({"time": time_str, "value": value})
        field_unit_map[field] = unit
        field_icon_map[field] = icon

        # 이상치 포함 여부
        if sensor_key in anomaly_sensor:
            field_abnormal_map[field] = True

    # 시계열 데이터 변환
    metrics = []
    for field, data in dataset.items():
        metrics.append(
            {
                "title": field,
                "icon": field_icon_map.get(field),
                "unit": field_unit_map.get(field),
                "normal": field_abnormal_map.get(field, False),
                "data": data,
            }
        )

    pprint.pprint(metrics)
    return metrics


def event_summary(df_event, df_sensor):
    """
    이벤트 데이터를 요약해주는 메소드입니다.
    """
    if (
        df_event.empty
        or "_time" not in df_event.columns
        or "event_type" not in df_event.columns
    ):
        return ["이벤트 데이터가 없습니다."]

    df_event = df_event.copy()
    df_event["_time"] = pd.to_datetime(df_event["_time"])

    start_date = df_sensor["_time"].min().strftime("%Y.%m.%d")
    end_date = df_sensor["_time"].max().strftime("%Y.%m.%d")

    # event_type이 'door_open'인 것만 필터링
    door_open_df = df_event[df_event["event_type"] == "door_open"]
    door_open_count = len(door_open_df)

    return [f"{start_date} ~ {end_date} 문열림 감지 이벤트 {door_open_count}회 발생"]
