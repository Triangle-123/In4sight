"""
컴프레서 압력 이상치를 판단하는 모듈입니다.
컴프레서 압력의 경우 0.8 ~ 1.2MPa 사이의 값을 가지면 정상입니다.

컴프레서 압력의 노이즈를 제거한 뒤, 이상치가 존재하는지를 확인하고
이상치가 존재한다면 어떤 범위에서 이상치가 존재하는지를 판단합니다.
"""

import logging

from scipy.signal import savgol_filter

logger = logging.getLogger(__name__)

MAX_PRESSURE = 1.2
MIN_PRESSURE = 0.8
WINDOW_LENGTH = 14
POLYORDER = 1


def detect_pressure_anomalies(df_sensor, anomaly_prompts, related_sensor):
    """
    컴프레서 압력 이상치를 판단합니다.
    """

    df_sensor = noise_filter(df_sensor)

    anormality_range = detect_anomalies_range(df_sensor)

    if anormality_range:
        logger.info("[컴프레서 압력 이상치 범위] %s", anormality_range)
        related_sensor.append("컴프레서 압력")

        for start, end in anormality_range:
            anomaly_prompts.append(f"[컴프레서 압력 이상치 범위] {start} ~ {end}")

    else:
        logger.info("[컴프레서 압력 정상] 압력 이상치 없음")


def noise_filter(df_sensor):
    """
    컴프레서 압력 데이터의 노이즈를 제거합니다.
    """

    y_filtered = savgol_filter(
        df_sensor["refrigerant_pressure"], WINDOW_LENGTH, POLYORDER
    )

    df_sensor["filtered_pressure"] = y_filtered

    return df_sensor


def detect_anomalies_range(df_sensor):
    """
    컴프레서 압력이 이상치를 가지는 범위를 판단합니다.
    """

    result = []

    if (
        df_sensor["filtered_pressure"].max() > MAX_PRESSURE
        or df_sensor["filtered_pressure"].min() < MIN_PRESSURE
    ):
        result = []
        countinues = False
        error_duration = {"start": None, "end": None}

        for i in range(len(df_sensor)):
            if (
                df_sensor["filtered_pressure"][i] > MAX_PRESSURE
                or df_sensor["filtered_pressure"][i] < MIN_PRESSURE
            ):
                if countinues:
                    error_duration["end"] = df_sensor["_time"].iloc[i]
                else:
                    error_duration["start"] = df_sensor["_time"].iloc[i]
                    countinues = True
            else:
                if countinues:
                    result.append([error_duration["start"], error_duration["end"]])
                countinues = False

        if countinues:
            result.append([error_duration["start"], df_sensor["_time"].iloc[-1]])

    return result
