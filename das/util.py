"""
Provides some arithmetic functions
"""

from datetime import datetime


def convert_to_iso_utc(date_str):
    """
    Provides some arithmetic functions
    """

    try:
        # 다양한 입력 포맷 처리
        formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"]
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError("Invalid date format")

        # UTC 기준 ISO 8601 포맷으로 변환
        return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    except Exception as e:  # pylint:disable=broad-except
        print(f"Error converting date: {e}")
        return None
