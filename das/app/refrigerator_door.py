"""
냉장고 문 관련 이상치를 판단하는 모듈입니다.
"""

import pandas as pd

from app.util import get_door_times

LIMIT_OPEN_NUMBER = 50


def check_door_anormality(df_event, anormality_list, related_sensor):
    """
    냉장실, 냉동실의 도어 센서 이상치를 판단하는 로직입니다.
    """

    df_event["_time"] = pd.to_datetime(df_event["_time"])
    df_event["date"] = df_event["_time"].dt.date  # 날짜만 추출

    door_abnormal_list = []

    # 날짜별 그룹화하여 리스트로 저장
    grouped_data = [group for _, group in df_event.groupby("date")]

    for group in grouped_data:
        find_door_anomality(group, door_abnormal_list)

    if door_abnormal_list:
        anormality_list.append((1, door_abnormal_list))
        related_sensor.append("냉장실 문")


def find_door_anomality(df_event, many_abnormal_list):
    """
    냉장실, 냉동실의 도어 센서 이상치 구간을 구하는 로직입니다.
    """

    open_times_fridge, close_times_fridge = get_door_times(df_event, "fridge")

    # 냉동실 문 이벤트
    open_times_freezer, close_times_freezer = get_door_times(df_event, "freezer")

    def check_location_door(location_name, open_times, close_times):
        open_number = len(open_times)
        max_interval = 0
        for ot, ct in zip(open_times, close_times):
            interval = int((ct - ot).value)  # ns 단위
            max_interval = max(max_interval, interval)

        # 문 열림 횟수 이상
        if open_number >= LIMIT_OPEN_NUMBER:
            start_str = df_event["date"].iloc[0]

            many_abnormal_list.append(
                f"{start_str}에 {location_name} 문열림이 {open_number}회 발생하였습니다."
            )

    # 냉장실과 냉동실 각각 검사
    check_location_door("냉장실", open_times_fridge, close_times_fridge)
    check_location_door("냉동실", open_times_freezer, close_times_freezer)
