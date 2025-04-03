"""
세탁기 시계열 데이터를 API 서버에 데이터를 보내는 형식으로 바꾸기 위한 모듈입니다.
"""

from app.api_data_refine import api_data_refine, refine_query_data

METRICS = {
    "water_level": "세탁기 내부 수위",
    "motor_current": "모터 전류 소비량",
    "voltage": "세탁기 내부 전압",
    "drum_rpm": "드럼 회전 속도",
    "vibration": "세탁기 진동 정도",
    "temperature": "세탁기 내부 온도",
    "weight": "세탁물 무게",
}

# 센서별 임계값 설정
SENSOR_THRESHOLDS = {
    "water_level": {"warning": 30, "critical": 35},
    "motor_current": {"warning": 1.3, "critical": 1.5},
    "voltage": {"warning": 240, "critical": 250},
    "drum_rpm": {"warning": 1000, "critical": 1100},
    "vibration": {"warning": 1.3, "critical": 1.5},
    "temperature": {"warning": 50, "critical": 60},
    "weight": {"warning": 10, "critical": 12},
}

# 센서별 그래프 min,max 값
SENSOR_MIN_MAX = {
    "water_level": {"min": 0, "max": 40},
    "motor_current": {"min": 0, "max": 1.6},
    "voltage": {"min": 200, "max": 260},
    "drum_rpm": {"min": 0, "max": 1200},
    "vibration": {"min": 0, "max": 1.6},
    "temperature": {"min": 10, "max": 65},
    "weight": {"warning": 0, "critical": 13},
}

UNIT = {
    "water_level": "cm",
    "motor_current": "A",
    "voltage": "V",
    "drum_rpm": "rpm",
    "vibration": "g",
    "temperature": "℃",
    "weight": "kg",
}

ICON = {
    "water_level": "Droplet",
    "motor_current": "Plug-2",
    "voltage": "Zap",
    "drum_rpm": "Disc-3",
    "vibration": "Vibrate",
    "temperature": "Thermometer",
    "weight": "Weight",
}

SENSOR_DATA_LIST = [
    "water_level",
    "motor_current",
    "voltage",
    "drum_rpm",
    "vibration",
    "temperature",
    "weight",
    "_time",
]

DEFAULT_DATA_LIST = ["_time"]


def get_wm_refine_data(df_sensor):
    """
    세탁기 시계열 데이터를 API 서버에 보낼 데이터를 정제하는 함수입니다.
    """

    sensor = refine_query_data(df_sensor, SENSOR_DATA_LIST, DEFAULT_DATA_LIST)

    return api_data_refine(
        sensor, [METRICS, SENSOR_THRESHOLDS, SENSOR_MIN_MAX, UNIT, ICON]
    )
