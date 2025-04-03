"""
API 서버와 데이터 형식을 맞추기 위해 데이터를 전처리하는 모듈입니다.
"""

import pprint
from collections import defaultdict
from json import loads


def determine_status(sensor_key, value, sensor_threshold, location=None):
    """
    센서 데이터의 상태를 결정하는 함수
    Args:
        sensor_key (str): 센서 키
        value (float): 센서 값
        location (str, optional): 위치 정보 (fridge 또는 freezer)
    Returns:
        int: 0 (정상), 1 (주의), 2 (경고)
    """
    threshold = sensor_threshold.get(sensor_key)
    if threshold is None:
        return 0

    # temp_internal의 경우 location에 따라 다른 임계값 적용
    if sensor_key == "temp_internal" and location:
        threshold = threshold.get(location)
        if threshold is None:
            return 0
        warning = threshold["warning"]
        critical = threshold["critical"]
    else:
        warning = threshold["warning"]
        critical = threshold["critical"]

    status = 0  # 기본값은 정상(0)

    # 냉매 압력의 경우 값이 낮을수록 문제
    if sensor_key == "refrigerant_pressure":
        if value <= critical:
            status = 2
        elif value <= warning:
            status = 1

    # 냉동실 온도의 경우 값이 높을수록 문제
    elif sensor_key == "temp_internal" and location == "freezer":
        if value >= critical:
            status = 2
        elif value >= warning:
            status = 1

    # 그 외 센서들은 값이 높을수록 문제
    else:
        if value >= critical:
            status = 2
        elif value >= warning:
            status = 1

    return status


def api_data_refine(df, device_info_list, anomaly_sensor=None):
    """
    API 서버에 보낼 데이터를 정제하는 함수입니다.
    """
    metrics_list = device_info_list[0]
    sensor_threshold = device_info_list[1]
    sensor_min_max = device_info_list[2]
    unit_list = device_info_list[3]
    icon_list = device_info_list[4]

    dataset = defaultdict(list)
    field_sensor_map = {}
    field_icon_map = {}
    field_unit_map = {}
    field_abnormal_map = {}

    # 리스트 형태의 데이터 처리
    for data in df:
        time_str = data["time"]
        sensor_key = data["sensor"]
        location_key = None
        if "location" in data:
            location_key = data.get("location")

        # 기본 센서명 → 한국어 필드명
        base_field_name = metrics_list.get(sensor_key)
        unit = unit_list.get(sensor_key)
        icon = icon_list.get(sensor_key)

        if location_key:
            prefix = metrics_list.get(location_key, "")
            field = f"{prefix} {base_field_name}"
        else:
            field = base_field_name

        value = data["value"]
        if sensor_key == "fan_rpm":
            value = int(value)

        # 상태 결정
        status = determine_status(sensor_key, value, sensor_threshold, location_key)

        # 시계열 데이터 쌓기
        dataset[field].append({"time": time_str, "value": value, "status": status})
        field_unit_map[field] = unit
        field_icon_map[field] = icon
        field_sensor_map[field] = sensor_key

        # 이상치 포함 여부
        if sensor_key in (anomaly_sensor or []):
            field_abnormal_map[field] = True

    metrics = []
    for field, data in dataset.items():
        sensor_key = field_sensor_map.get(field)
        location = None
        if "냉장실" in field:
            location = "fridge"
        elif "냉동실" in field:
            location = "freezer"

        # temp_internal의 경우 location에 따라 다른 임계값 적용
        if sensor_key == "temp_internal" and location:
            thresholds = sensor_threshold.get(sensor_key, {}).get(location, {})
            min_max = sensor_min_max.get(sensor_key, {}).get(location, {})
        else:
            thresholds = sensor_threshold.get(sensor_key, {})
            min_max = sensor_min_max.get(sensor_key, {})

        metrics.append(
            {
                "title": field,
                "icon": field_icon_map.get(field),
                "unit": field_unit_map.get(field),
                "lower_bound": min_max.get("min", 0),
                "upper_bound": min_max.get("max", 100),
                "warning_threshold": thresholds.get("warning"),
                "danger_threshold": thresholds.get("critical"),
                "normal": not field_abnormal_map.get(field, False),
                "data": data,
            }
        )

    pprint.pprint(metrics)
    return metrics


def refine_query_data(df_sensor, sensor_data_list, default_data_list):
    """
    data_frame 형식의 데이터를 dictionary 형태로 바꾸기 위한 함수입니다.
    """

    sensor = df_sensor[sensor_data_list].sort_values(["_time"])

    # 3. melt용 ID 컬럼 확인
    id_vars = [col for col in default_data_list if col in sensor.columns]

    # 4. melt
    sensor = sensor.melt(id_vars=id_vars, var_name="sensor", value_name="value").rename(
        columns={"_time": "time"}
    )

    # value가 null인 행 제거
    sensor = sensor.dropna(subset=["value"])

    sensor = loads(sensor.to_json(orient="records", date_format="iso", date_unit="s"))

    return sensor
