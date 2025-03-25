"""
냉장고 냉기 토출구 팬 관련 이상치를 판단하는 모듈입니다.
"""

from datetime import timedelta

LIMIT_OPEN_NUMBER = 50
LIMIT_MAX_INTERVAL = 20 * 60 * 10**9  # 20분을 나노초로 환산
HIGH_RPM_THRESHOLD = 1400  # RPM 임계값
MIN_DURATION_MINUTES = 30  # 최소 지속 시간 (분)


def check_fan_rpm_anormality(df_event, anormality_list, related_sensor):
    """
    냉장고 냉기 토출구 팬 이상치를 판단하는 로직입니다.

    Args:
        df_event (DataFrame): 팬 RPM 데이터가 포함된 DataFrame
        anormality_list (list): 감지된 이상 상태를 저장할 리스트
        related_sensor (list): 관련된 센서 정보를 저장할 리스트

    Returns:
        None
    """
    # 임계값 이상인 데이터의 인덱스 찾기
    high_rpm_indices = df_event[df_event["fan_rpm"] >= HIGH_RPM_THRESHOLD].index

    if len(high_rpm_indices) == 0:
        return

    # 연속된 인덱스 그룹화
    chunks = []
    current_chunk = [high_rpm_indices[0]]

    for i in range(1, len(high_rpm_indices)):
        if high_rpm_indices[i] - high_rpm_indices[i - 1] == 1:
            current_chunk.append(high_rpm_indices[i])
        else:
            if len(current_chunk) > 0:
                chunks.append(current_chunk)
            current_chunk = [high_rpm_indices[i]]

    if len(current_chunk) > 0:
        chunks.append(current_chunk)

    # 각 청크 처리
    for chunk in chunks:
        start_time = df_event.iloc[chunk[0]]["_time"]
        end_time = df_event.iloc[chunk[-1]]["_time"]
        duration = end_time - start_time

        # 지속 시간이 MIN_DURATION_MINUTES 이상인 경우만 처리
        if duration >= timedelta(minutes=MIN_DURATION_MINUTES):
            avg_rpm = df_event.iloc[chunk]["fan_rpm"].mean()
            duration_minutes = duration.total_seconds() / 60

            # 시간 형식 변환
            hours = int(duration_minutes // 60)
            minutes = int(duration_minutes % 60)

            date_str = f"{start_time.year}년 {start_time.month}월 {start_time.day}일"
            time_str = f"{start_time.hour:02d}:{start_time.minute:02d}"

            # 이상 상태 메시지 생성
            if hours > 0:
                duration_str = f"{hours}시간 {minutes}분"
            else:
                duration_str = f"{minutes}분"

            message = (
                f"{date_str} {time_str}부터 {duration_str} 동안 "
                f"팬 RPM이 높게 유지되었습니다 (평균 {avg_rpm:.1f} RPM)."
            )

            anormality_list.append(message)
            related_sensor.append("냉기토출구_팬RPM")
