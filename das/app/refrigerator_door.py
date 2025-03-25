"""
냉장고 문 관련 이상치를 판단하는 모듈입니다.
"""

from app.util import get_door_times

LIMIT_OPEN_NUMBER = 50
LIMIT_MAX_INTERVAL = 20 * 60 * 10**9  # 20분을 나노초로 환산


def check_door_anormality(df_event, anormality_list, related_sensor):
    """
    냉장실, 냉동실의 도어 센서 이상치를 판단하는 로직입니다.
    """
    # 냉장실 문 이벤트
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
            anormality_list.append(f"{location_name} 문 열림 횟수가 너무 많음")
            related_sensor.append("문")

    # 냉장실과 냉동실 각각 검사
    check_location_door("냉장실", open_times_fridge, close_times_fridge)
    check_location_door("냉동실", open_times_freezer, close_times_freezer)
