"""
다수의 모듈에서 사용하는 함수들을 모아놓은 곳입니다.
"""

from datetime import datetime, timedelta


def convert_to_iso_utc(date_str):
    """
    다양한 시간 입력 포맷을 일관되게 처리해줍니다.
    """
    # 지원하는 입력 포맷
    formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt) - timedelta(hours=9)
            break
        except ValueError:
            continue
    else:
        print("Error converting date: Invalid date format")
        return None

    # UTC 기준 ISO 8601 포맷으로 변환
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def get_door_times(df_event, location):
    """
    지정한 location에 해당하는 문 이벤트의 open/close 시간 리스트를 반환합니다.
    """
    df_loc = df_event[df_event["location"] == location]
    open_times = list(df_loc[df_loc["event_type"] == "door_open"]["_time"])
    close_times = list(df_loc[df_loc["event_type"] == "door_close"]["_time"])
    return open_times, close_times
