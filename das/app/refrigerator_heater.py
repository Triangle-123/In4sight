"""
    냉장고 히터 센서의 이상치를 감지하는 로직입니다.
"""

import pandas as pd
from datetime import timedelta
import logging

logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%Y/%m/%d %I:%M:%S%p',
    level=logging.INFO
)

def detect_heater_anomalies(df_sensor, anomaly_prompts, related_sensor, anomaly_sensors):
    threshold_temp = 50         # 이상 판단 기준 온도
    min_duration = 3            # 15분 간격 x 3 = 45분
    high_temp_streaks = []      # 고온 구간 리스트
    current_streak = []         # 현재 고온 연속 리스트

    logging.debug("[히터 감지] 센서 데이터 총 개수: %d", len(df_sensor))

    # 연속 고온 구간 탐지
    for i in range(len(df_sensor)):
        temp = df_sensor.iloc[i, "heater_temp"]
        if temp >= threshold_temp:
            current_streak.append(df_sensor.iloc[i])
        else:
            if len(current_streak) >= min_duration:
                high_temp_streaks.append(current_streak)
                logging.debug("[고온 지속 감지] streak 추가 (길이: %d)", len(current_streak))
            current_streak = []

    # 마지막 streak 추가 여부 확인
    if len(current_streak) >= min_duration:
        high_temp_streaks.append(current_streak)
        logging.debug("[고온 지속 감지] 마지막 streak 추가 (길이: %d)", len(current_streak))

    num_high_streaks = len(high_temp_streaks)
    high_temp_outside_defrost = 0
    outside_defrost_ranges = []
    new_high_temp_streaks = []

    for streak in high_temp_streaks:
        timestamps = [pd.to_datetime(record["_time"]) for record in streak]
        timestamps_kst = [ts + timedelta(hours=9) for ts in timestamps]
        hours = [ts.hour for ts in timestamps_kst]

        logging.debug("[시간 변환] UTC: %s", timestamps)
        logging.debug("[시간 변환] KST: %s", timestamps_kst)
        logging.debug("[시간 검토] KST 시각: %s", hours)

        # 제상 시간(6시~7시)에만 해당하면 정상
        if not all(6 <= hour <= 7 for hour in hours):
            start_time = min(timestamps_kst)
            end_time = max(timestamps_kst)

            logging.info("[제상 시간 외 고온 구간] %s ~ %s", start_time.isoformat(), end_time.isoformat())
            outside_defrost_ranges.append((start_time, end_time))
            high_temp_outside_defrost += 1
        else:
            new_high_temp_streaks.append(streak)

    high_temp_streaks = new_high_temp_streaks

    # 최종 이상 판단
    is_abnormal = num_high_streaks >= 3 or high_temp_outside_defrost >= 1

    if is_abnormal:
        result_msg = f"[히터 센서 이상] 고온 지속 구간: {num_high_streaks}회, 제상 시간 외 고온: {high_temp_outside_defrost}회"
        logging.info(result_msg)

        anomaly_prompts.append(result_msg)
        related_sensor.append("히터")
        anomaly_sensors.append("heater_temp")

        logging.debug("관련 센서 추가됨: %s", related_sensor)
        logging.debug("이상 항목 추가됨: %s", anomaly_sensors)
    else:
        logging.info("[히터 센서 정상] 이상 없음.")


