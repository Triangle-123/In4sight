"""
API 서버에 데이터를 보내는 형식으로 바꾸기 위한 모듈입니다.
"""

from collections import defaultdict

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


def api_data_refine(df):
    """
    데이터 필드별로 묶어서 데이터를 전송하기 위한 전처리 함수입니다.
    """
    dataset = defaultdict(list)
    field_unit_map = {}

    for data in df:
        time_str = data["time"]  # ISO 형식의 시간 문자열 변환
        field = METRICS[data["sensor"]]
        unit = UNIT[data["sensor"]]

        if data["location"]:
            field = f'{METRICS[data["location"]]} ' + field

        dataset[field].append({"time": time_str, "value": data["value"]})
        field_unit_map[field] = unit

    # 변환된 JSON 데이터 생성
    dataset = [
        {"title": field, "unit": field_unit_map[field], "data": data}
        for field, data in dataset.items()
    ]

    return dataset
