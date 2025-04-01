"""
컴프레서 압력 이상치를 판단하는 모듈입니다.
컴프레서 압력의 경우 0.8 ~ 1.2MPa 사이의 값을 가지면 정상입니다.

컴프레서 압력의 노이즈를 제거한 뒤, 이상치가 존재하는지를 확인하고
이상치가 존재한다면 어떤 범위에서 이상치가 존재하는지를 판단합니다.
"""

import logging

from scipy.signal import savgol_filter

from app.util import detect_anomalies_range, make_event_set

logger = logging.getLogger(__name__)

MAX_PRESSURE = 1.2
MIN_PRESSURE = 0.8
WINDOW_LENGTH = 14
POLYORDER = 1


def detect_pressure_anomalies(
    df_sensor, anomaly_prompts, related_sensor, anomaly_sensor
):
    """
    컴프레서 압력 이상치를 판단합니다.
    """

    df_sensor = noise_filter(df_sensor)

    anormality_range = detect_anomalies_range(
        df_sensor, "refrigerant_pressure", MAX_PRESSURE, MIN_PRESSURE
    )

    if anormality_range:
        logger.info("[컴프레서 압력 이상치 범위] %s", anormality_range)
        related_sensor.append("컴프레서 압력")

        eventset = make_event_set(anormality_range, "컴프레서 압력이 높았습니다.")
        if eventset:
            anomaly_prompts.append((0, eventset))
            anomaly_sensor.append("refrigerant_pressure")
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
