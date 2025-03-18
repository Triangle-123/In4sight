"""
이 모듈은 날짜만 입력해도 influxDB 쿼리문에서 사용할 수 있게 포맷팅 해주는 모듈입니다.
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
