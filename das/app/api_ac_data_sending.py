"""
에어컨 시계열 데이터를 API 서버에 데이터를 보내는 형식으로 바꾸기 위한 모듈입니다.
"""

from app.api_data_refine import api_data_refine, refine_query_data

METRICS = {
    "evaporator_humidity": "증발기 주변 습도",
    "external_humidity": "외부 습도",
    "filter_dust": "필터 오염 정도",
    "refrigerant_pressure": "냉매 압력",
    "refrigerant_temp": "냉매 온도",
    "room_temp": "실내 온도",
}

# 센서 컬럼명과 한글 매핑
MEASUREMENT_NAMES = {
    "evaporator_humidity": "습도",
    "external_humidity": "습도",
    "filter_dust": "오염도",
    "refrigerant_pressure": "압력",
    "refrigerant_temp": "온도",
    "room_temp": "온도",
}

# 센서별 임계값 설정
SENSOR_THRESHOLDS = {
    "evaporator_humidity": {"warning": 90, "critical": 95},
    "external_humidity": {"warning": 80, "critical": 90},
    "filter_dust": {"warning": 50, "critical": 70},
    #   "refrigerant_pressure": {"warning": None, "critical": None},
    "refrigerant_pressure": {"warning": 0.4, "critical": 0.2},
    "refrigerant_temp": {"warning": 60, "critical": 70},
    "room_temp": {"warning": 35, "critical": 40},
}

# SENSOR_THRESHOLDS_LOW = {
#     "evaporator_humidity": {"warning": None, "critical": None},
#     "external_humidity": {"warning": None, "critical": None},
#     "filter_dust": {"warning": None, "critical": None},
#     "refrigerant_pressure": {"warning": 0.4, "critical": 0.2},
#     "refrigerant_temp": {"warning": None, "critical": None},
#     "room_temp": {"warning": None, "critical": None},
# }

# SENSOR_THRESHOLDS = [SENSOR_THRESHOLDS_HIGH, SENSOR_THRESHOLDS_LOW]

# 센서별 그래프 min,max 값
SENSOR_MIN_MAX = {
    "evaporator_humidity": {"min": 0, "max": 100},
    "external_humidity": {"min": 0, "max": 100},
    "filter_dust": {"min": 0, "max": 80},
    "refrigerant_pressure": {"min": 0, "max": 1},
    "refrigerant_temp": {"min": 10, "max": 80},
    "room_temp": {"min": 10, "max": 50},
}

UNIT = {
    "evaporator_humidity": "%",
    "external_humidity": "%",
    "filter_dust": "µg/m³",
    "refrigerant_pressure": "bar",
    "refrigerant_temp": "℃",
    "room_temp": "℃",
}

ICON = {
    "evaporator_humidity": "Droplets",
    "external_humidity": "Droplet",
    "filter_dust": "Factory",
    "refrigerant_pressure": "CircleGauge",
    "refrigerant_temp": "ThermometerSnowflake",
    "room_temp": "ThermometerSun",
}

AC_SENSOR_DATA_LIST = [
    "evaporator_humidity",
    "external_humidity",
    "filter_dust",
    "refrigerant_pressure",
    "refrigerant_temp",
    "room_temp",
    "_time",
]

DEFAULT_DATA_LIST = ["_time"]


def get_ac_refine_data(df_sensor):
    """
    에어컨 시계열 데이터를 API 서버에 보낼 데이터를 정제하는 함수입니다.
    """

    sensor = refine_query_data(df_sensor, AC_SENSOR_DATA_LIST, DEFAULT_DATA_LIST)

    return api_data_refine(
        sensor,
        [METRICS, SENSOR_THRESHOLDS, SENSOR_MIN_MAX, UNIT, ICON, MEASUREMENT_NAMES],
    )
