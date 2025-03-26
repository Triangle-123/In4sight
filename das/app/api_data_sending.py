"""
API 서버에 데이터를 보내는 형식으로 바꾸기 위한 모듈입니다.
"""

from collections import defaultdict


def api_data_refine(df):
    """
    데이터 필드별로 묶어서 데이터를 전송하기 위한 전처리 함수입니다.
    """
    dataset = defaultdict(list)

    for data in df:
        time_str = data["time"]  # ISO 형식의 시간 문자열 변환
        field = data["sensor"]

        if data["location"]:
            field += f'_{data["location"]}'

        dataset[field].append({"time": time_str, "value": data["value"]})

    # 변환된 JSON 데이터 생성
    dataset = [{"field": field, "data": data} for field, data in dataset.items()]

    return dataset
