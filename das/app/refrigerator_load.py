"""
냉장고 적재량 관련 이상치를 판단하는 모듈입니다.
"""

import logging

from app.util import detect_anomalies_range, make_event_set

# from datetime import timedelta

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y/%m/%d %I:%M:%S%p",
    level=logging.INFO,
)

THRESHOLD_LOAD = 85


def check_loading_rate_anormality(
    df_sensor, anormality_list, related_sensor, anomaly_sensor
):
    """
    냉장고 적재량 이상치를 판단하는 로직입니다.
    """

    df_fridge = df_sensor[df_sensor["location"] == "fridge"]
    df_freezer = df_sensor[df_sensor["location"] == "freezer"]

    high_fridge_load_range = detect_anomalies_range(
        df_fridge, "load_percent", THRESHOLD_LOAD, -1
    )

    high_freezer_load_range = detect_anomalies_range(
        df_freezer, "load_percent", THRESHOLD_LOAD, -1
    )

    if high_fridge_load_range:
        eventset = make_event_set(
            high_fridge_load_range, "냉장실 내 적재량이 많았습니다."
        )

        if eventset:
            anormality_list.append((4, eventset))
            related_sensor.append("냉장실 적재량")
            anomaly_sensor.append("load")

    if high_freezer_load_range:
        eventset = make_event_set(
            high_fridge_load_range, "냉동실 내 적재량이 많았습니다."
        )

        if eventset:
            anormality_list.append((11, eventset))
            related_sensor.append("냉동실 적재량")
            anomaly_sensor.append("load")
