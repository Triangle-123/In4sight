"""
냉장고 시계열 데이터를 API 서버에 데이터를 보내는 형식으로 바꾸기 위한 모듈입니다.
"""

from app.api_data_refine import api_data_refine, refine_query_data

METRICS = {
    "fan_rpm": "팬 속도",
    "heater_temp": "히터 온도",
    "load_percent": "적재량",
    "refrigerant_pressure": "압력 센서",
    "temp_external": "외부 온도",
    "temp_internal": "내부 온도",
    "fridge": "냉장실",
    "freezer": "냉동실",
    "door_open": "문열림",
    "defrost_cycle": "제상 사이클 진행",
    "load_change": "적재량 변화",
}

# 센서 컬럼명과 한글 매핑
MEASUREMENT_NAMES = {
    "fan_rpm": "속도",
    "heater_temp": "온도",
    "load_percent": "적재량",
    "refrigerant_pressure": "압력",
    "temp_external": "온도",
    "temp_internal": "온도",
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

LOCATION_EVENT_DATA_LIST = ["door_open", "load_change"]

SIMPLE_EVENT_DATA_LIST = ["defrost_cycle"]


def get_ref_refine_data(df_sensor):
    """
    API 서버에 보낼 데이터를 정제하는 함수입니다.
    """

    sensor = refine_query_data(df_sensor, SENSOR_DATA_LIST, DEFAULT_DATA_LIST)
    return api_data_refine(
        sensor,
        [METRICS, SENSOR_THRESHOLDS, SENSOR_MIN_MAX, UNIT, ICON, MEASUREMENT_NAMES],
    )


def event_summary(df_event):
    """
    문 열림 이벤트 데이터를 요약해주는 메소드입니다.
    """

    event_dataset = []
    for event in LOCATION_EVENT_DATA_LIST:
        target_df_event = df_event[df_event["event_type"] == event]

        for location in EVENT_LOCATION:
            target_location_df_event = target_df_event[
                target_df_event["location"] == location
            ]
            event_data = {}
            event_data["field"] = f"{event}_{location}"
            event_data["measurement"] = f"{METRICS[location]} {METRICS[event]}"
            event_data["time"] = [
                d.strftime("%Y-%m-%d %H:%M:%S")
                for d in target_location_df_event["_time"]
            ]

            event_dataset.append(event_data)

    for event in SIMPLE_EVENT_DATA_LIST:
        event_data = {}
        target_df_event = df_event[df_event["event_type"] == event]

        event_data["field"] = f"{event}"
        event_data["measurement"] = f"{METRICS[event]}"
        event_data["time"] = [
            d.strftime("%Y-%m-%d %H:%M:%S") for d in target_df_event["_time"]
        ]

        print(event_data)
        event_dataset.append(event_data)

    return event_dataset
