"""
API 서버와 데이터 형식을 맞추기 위해 데이터를 전처리하는 모듈입니다.
"""

from collections import defaultdict
from json import loads


def api_data_refine(df, device_info_list):
    """
    API 서버에 보낼 데이터를 정제하는 함수입니다.
    """
    metrics_list = device_info_list[0]
    sensor_threshold = device_info_list[1]
    sensor_min_max = device_info_list[2]
    unit_list = device_info_list[3]
    icon_list = device_info_list[4]
    measurement_names = device_info_list[5]

    dataset = defaultdict(list)
    field_sensor_map = {}
    field_icon_map = {}
    field_unit_map = {}

    # 리스트 형태의 데이터 처리
    for data in df:
        time_str = data["time"]
        sensor_key = data["sensor"]
        location_key = data.get("location") if "location" in data else None

        # 기본 센서명 → 한국어 필드명
        base_field_name = metrics_list.get(sensor_key)
        unit = unit_list.get(sensor_key)
        icon = icon_list.get(sensor_key)

        field = (
            f"{metrics_list.get(location_key, '')} {base_field_name}"
            if location_key
            else base_field_name
        )

        value = int(data["value"]) if sensor_key == "fan_rpm" else data["value"]

        # 시계열 데이터 쌓기
        dataset[field].append({"time": time_str, "value": value})
        field_unit_map[field] = unit
        field_icon_map[field] = icon
        field_sensor_map[field] = sensor_key

    sensor_data = []
    for field, data in dataset.items():
        sensor_key = field_sensor_map.get(field)
        location = (
            "fridge" if "냉장실" in field else "freezer" if "냉동실" in field else None
        )

        # temp_internal의 경우 location에 따라 다른 임계값 적용
        if sensor_key == "temp_internal" and location:
            thresholds = sensor_threshold.get(sensor_key, {}).get(location, {})
            min_max = sensor_min_max.get(sensor_key, {}).get(location, {})
        else:
            thresholds = sensor_threshold.get(sensor_key, {})
            min_max = sensor_min_max.get(sensor_key, {})

        # 시계열 데이터 분리
        times = [d["time"] for d in data]
        values = [d["value"] for d in data]

        sensor_data.append(
            {
                "title": field,
                "measurement": measurement_names.get(sensor_key, sensor_key),
                "icon": field_icon_map.get(field),
                "unit": field_unit_map.get(field),
                "criteria": {
                    "lower_limit": min_max.get("min", 0),
                    "upper_limit": min_max.get("max", 100),
                    "threshold": {
                        "warning": thresholds.get("warning"),
                        "critical": thresholds.get("critical"),
                    },
                },
                "sensorName": f"{sensor_key}_{location}" if location else sensor_key,
                "data": {"time": times, "value": values},
            }
        )

    return sensor_data


def refine_query_data(df_sensor, sensor_data_list, default_data_list):
    """
    data_frame 형식의 데이터를 dictionary 형태로 바꾸기 위한 함수입니다.
    """
    sensor = df_sensor[sensor_data_list].sort_values(["_time"])
    id_vars = [col for col in default_data_list if col in sensor.columns]
    sensor = sensor.melt(id_vars=id_vars, var_name="sensor", value_name="value").rename(
        columns={"_time": "time"}
    )
    sensor = sensor.dropna(subset=["value"])

    sensor = loads(sensor.to_json(orient="records", date_format="iso", date_unit="s"))

    return sensor
