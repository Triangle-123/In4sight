"""
냉장고 냉기 토출구 팬 관련 이상치를 판단하는 모듈입니다.
"""

import logging
from datetime import timedelta

HIGH_RPM_THRESHOLD = 1400  # RPM 임계값
MIN_DURATION_MINUTES = 30  # 최소 지속 시간 (분)

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y/%m/%d %I:%M:%S%p",
    level=logging.INFO,
)


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
    high_rpm_indices = df_event[df_event["fan_rpm"] >= HIGH_RPM_THRESHOLD].index

    logging.debug("[팬 RPM 검사] 전체 데이터 수: %d", len(df_event))
    logging.debug("[팬 RPM 검사] 임계치 이상 데이터 수: %d", len(high_rpm_indices))

    if len(high_rpm_indices) == 0:
        logging.info("[팬 RPM 정상] 고속 회전 상태 없음.")
        return

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

    logging.info("[팬 RPM 검사] 고속 회전 연속 구간 수: %d", len(chunks))

    for chunk in chunks:
        start_time = df_event.iloc[chunk[0]]["_time"] + timedelta(hours=9)
        end_time = df_event.iloc[chunk[-1]]["_time"] + timedelta(hours=9)
        duration = end_time - start_time

        logging.debug(
            "[RPM 구간] 시작: %s, 종료: %s, 구간 길이: %s",
            start_time,
            end_time,
            duration,
        )

        if duration >= timedelta(minutes=MIN_DURATION_MINUTES):
            avg_rpm = df_event.iloc[chunk]["fan_rpm"].mean()
            duration_minutes = duration.total_seconds() / 60
            hours = int(duration_minutes // 60)
            minutes = int(duration_minutes % 60)

            date_str = f"{start_time.year}년 {start_time.month}월 {start_time.day}일"
            time_str = f"{start_time.hour:02d}:{start_time.minute:02d}"

            duration_str = f"{hours}시간 {minutes}분" if hours > 0 else f"{minutes}분"

            message = (
                f"{date_str} {time_str}부터 {duration_str} 동안 "
                f"팬 RPM이 높게 유지되었습니다 (평균 {avg_rpm:.1f} RPM)."
            )

            logging.info("[팬 RPM 이상 감지] %s", message)

            anormality_list.append(message)
            related_sensor.append("냉기토출구_팬RPM")

            logging.info(anormality_list)
        else:
            logging.debug(
                "[RPM 구간 무시됨] 지속 시간 %d분 < %d분",
                duration.total_seconds() / 60,
                MIN_DURATION_MINUTES,
            )
