"""
냉장고 시계열 데이터를 API 서버에 데이터를 보내는 형식으로 바꾸기 위한 모듈입니다.
"""

import pandas as pd

from app.api_data_refine import api_data_refine, refine_query_data

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

# 센서별 임계값 설정
SENSOR_THRESHOLDS = {
    "temp_internal": {
        "fridge": {"warning": 8, "critical": 12},  # 냉장실 온도 임계값
        "freezer": {"warning": -15, "critical": -17},  # 냉동실 온도 임계값
    },
    "temp_external": {"warning": 35, "critical": 40},  # 외부 온도 임계값
    "load_percent": {"warning": 75, "critical": 85},  # 부하율 임계값
    "refrigerant_pressure": {"warning": 0.8, "critical": 0.6},  # 냉매 압력 임계값
    "fan_rpm": {"warning": 1300, "critical": 1500},  # 팬 RPM 임계값
    "heater_temp": {"warning": 60, "critical": 70},  # 히터 온도 임계값
}

# 센서별 그래프 min,max 값
SENSOR_MIN_MAX = {
    "temp_internal": {
        "fridge": {"min": 0, "max": 30},
        "freezer": {"min": -20, "max": 0},
    },
    "temp_external": {"min": 10, "max": 50},
    "load_percent": {"min": 0, "max": 100},
    "refrigerant_pressure": {"min": 0, "max": 2},
    "fan_rpm": {"min": 800, "max": 1700},
    "heater_temp": {"min": 0, "max": 80},
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

EVENT_LOCATION = ["fridge", "freezer"]

SENSOR_DATA_LIST = [
    "temp_internal",
    "temp_external",
    "load_percent",
    "refrigerant_pressure",
    "fan_rpm",
    "heater_temp",
    "_time",
    "location",
]

DEFAULT_DATA_LIST = ["_time", "location"]


def get_ref_refine_data(df_sensor, anomaly_sensor=None):
    """
    API 서버에 보낼 데이터를 정제하는 함수입니다.
    """

    sensor = refine_query_data(df_sensor, SENSOR_DATA_LIST, DEFAULT_DATA_LIST)
    return api_data_refine(
        sensor, [METRICS, SENSOR_THRESHOLDS, SENSOR_MIN_MAX, UNIT, ICON], anomaly_sensor
    )


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

    event_dataset = []

    for location in EVENT_LOCATION:
        door_open_count = len(door_open_df[door_open_df["location"] == location])
        event_dataset.append(
            f"{start_date} ~ {end_date} {METRICS[location]} 문열림 감지 이벤트 {door_open_count}회 발생"
        )

    return event_dataset
