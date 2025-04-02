"""
냉장고 히터 센서의 이상치를 감지하는 로직입니다.
"""

import logging

import pandas as pd

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y/%m/%d %I:%M:%S%p",
    level=logging.INFO,
)

THRESHOLD_HEATHER = 50  # 이상 판단 기준 온도
MIN_DURATION = 3  # 15분 간격 x 3 = 45분

DEFROST_START_TIME = 6
DEFROST_END_TIME = 7


def detect_heater_anomalies(df_sensor, anomaly_prompts, related_sensor, anomaly_sensor):
    """
    히터 센서 온도 데이터를 분석하여 고온 지속 또는 제상 시간 외 고온 구간을 감지하고,
    이상 여부를 anomaly 목록에 기록합니다.
    """
    df_sensor["_time"] = pd.to_datetime(df_sensor["_time"])
    df_sensor["date"] = df_sensor["_time"].dt.date  # 날짜만 추출

    many_abnormal_list = []
    none_abnormal_list = []

    # 날짜별 그룹화하여 리스트로 저장
    grouped_data = [group for _, group in df_sensor.groupby("date")]

    logging.debug("[히터 감지] 센서 데이터 총 개수: %d", len(df_sensor["heater_temp"]))

    for group in grouped_data:
        if len(group) > 32:
            find_heater_anomality(group, many_abnormal_list, none_abnormal_list)

    if many_abnormal_list:
        anomaly_prompts.append((3, many_abnormal_list))
        related_sensor.append("히터")
        anomaly_sensor.append("heater_temp")

        logging.debug("관련 센서 추가됨: %s", related_sensor)

    if none_abnormal_list:
        anomaly_prompts.append((10, none_abnormal_list))
        related_sensor.append("히터")
        anomaly_sensor.append("heater_temp")

    else:
        logging.info("[히터 센서 정상] 이상 없음.")


def find_heater_anomality(df_sensor, many_abnormal_list, none_abnormal_list):
    """
    히터 센서 온도 이상치 구간을 구하는 함수입니다.
    """
    high_temp_streaks = []  # 고온 구간 리스트
    current_streak = []  # 현재 고온 연속 리스트

    # 연속 고온 구간 탐지
    for i in range(len(df_sensor)):
        temp = df_sensor.iloc[i]["heater_temp"]
        if temp >= THRESHOLD_HEATHER:
            current_streak.append(df_sensor.iloc[i])
        else:
            if len(current_streak) >= MIN_DURATION:
                high_temp_streaks.append(current_streak)
                logging.debug(
                    "[고온 지속 감지] streak 추가 (길이: %d)", len(current_streak)
                )
            current_streak = []

    # 마지막 streak 추가 여부 확인
    if len(current_streak) >= MIN_DURATION:
        high_temp_streaks.append(current_streak)
        logging.debug(
            "[고온 지속 감지] 마지막 streak 추가 (길이: %d)", len(current_streak)
        )

    num_high_streaks = len(high_temp_streaks)
    high_temp_outside_defrost = 0
    outside_defrost_ranges = []
    new_high_temp_streaks = []

    for streak in high_temp_streaks:
        timestamps = [pd.to_datetime(record["_time"]) for record in streak]
        timestamps_kst = list(timestamps)
        hours = [ts.hour for ts in timestamps_kst]

        # 제상 시간(6시~7시)에만 해당하면 정상
        if not all(DEFROST_START_TIME <= hour <= DEFROST_END_TIME for hour in hours):
            start_time = min(timestamps_kst)
            end_time = max(timestamps_kst)

            logging.info(
                "[제상 시간 외 고온 구간] %s ~ %s",
                start_time.isoformat(),
                end_time.isoformat(),
            )
            outside_defrost_ranges.append((start_time, end_time))
            high_temp_outside_defrost += 1
        else:
            logging.debug(
                "[정상 제상 시간] 고온이지만 제상 시간(6~7시)에 해당: %s",
                timestamps_kst,
            )
            new_high_temp_streaks.append(streak)

    high_temp_streaks = new_high_temp_streaks
    date = df_sensor["date"].iloc[0]

    # 최종 이상 판단
    is_abnormal = num_high_streaks >= 3 or high_temp_outside_defrost >= 1

    if is_abnormal:
        abnormal_list = []

        for start, end in high_temp_streaks:
            event_string = (
                f"{date} {start} ~ {end}시에 예상되지 않은 제상 작업이 진행되었습니다."
            )

            abnormal_list.append(event_string)

        many_abnormal_list += abnormal_list

    if num_high_streaks == 0:
        none_abnormal_list.append(
            f"{date}에 예정되었던 제상 작업이 진행되지 않았습니다."
        )
