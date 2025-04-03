"""
RAG 서버에 보내는 메시지 형식으로 바꿔서 broadcast하는 module 입니다.
"""

import eda


def check_scenario(anomality_list):
    """
    시나리오 별로 부여된 수를 반환하는 함수입니다.
    """

    scenario_number = 0

    for number in anomality_list:
        scenario_number += 1 << number

    return scenario_number


def insert_event(anomality_number, anomality_list):
    """
    이벤트 내용을 응답으로 보내줄 이벤트 리스트에 넣어주는 함수입니다.
    """
    for number, eventset in anomality_list:
        if number == anomality_number:
            return eventset

    return []


ANOMALITY = [
    "컴프레서 압력에 이상치가 감지되었습니다.",
    "과도한 문 개폐 이벤트가 감지되었습니다.",
    "냉기 토출구 팬 RPM이 높은 구간이 감지되었습니다.",
    "제상 시간 외 히터 고온 구간이 감지되었습니다.",
    "냉장실에 과도하게 적재한 구간이 감지되었습니다.",
    "냉장실 내부 온도가 높은 구간이 감지되었습니다.",
    "냉장실에 뜨거운 음식을 넣었을 가능성이 있습니다.",
    "냉동실 내부 온도가 높은 구간이 감지되었습니다",
    "외부 온도가 너무 낮습니다.",
    "외부 온도가 너무 높습니다",
    "제상 사이클이 작동하지 않았습니다.",
    "냉동실에 과도하게 적재한 구간이 감지되었습니다.",
]

RELATED_SENSOR = [
    "컴프레서 압력",
    "문",
    "냉기 토출구 팬 RPM",
    "히터",
    "적재량",
    "냉장실 내부 온도",
    "냉장실 내부 온도",
    "냉동실 내부 온도",
    "외부 온도",
    "외부 온도",
    "히터",
]

EXPECTED_SYMPTOM = [
    "냉장실 내부 온도가 높습니다.(냉매 누출)",
    "냉장실 내부 온도가 높습니다.(과도한 문 개폐 이벤트)",
    "냉장실 내부 온도가 높습니다.(제상 사이클 이상)",
    "냉장실 내부 온도가 높습니다.(냉장실 공간 부족 등으로 냉기 토출구 막힘)",
    "냉장실 내부 온도가 높습니다.(뜨거운 음식 보관)",
    "냉장실 내부 음식이 업니다.",
    "냉장실에 성에가 낍니다.",
    "냉장고 소음이 심합니다.",
    "냉동실에 넣어둔 음식이 녹습니다.(냉매 누출)",
    "냉동실에 넣어둔 음식이 녹습니다.(제상 사이클 이상)",
]

SYMPTOM_CHECK = [
    [check_scenario([0])],
    [check_scenario([1])],
    [check_scenario([3]), check_scenario([10])],
    [check_scenario([2]), check_scenario([4])],
    [check_scenario([6])],
    [check_scenario([2])],
    [check_scenario([10])],
    [check_scenario([2])],
    [check_scenario([0]), check_scenario([0, 7])],
    [
        check_scenario([3]),
        check_scenario([10]),
        check_scenario([3, 7]),
        check_scenario([10, 7]),
    ],
]

INTERNAL_TEMP_INDEX = 5
HIGH_INTENAL_TEMP_SYMPTOM_INDEX = 5
ANOMALITY_NUMBER = len(ANOMALITY)
SYMPTOM_NUMBER = len(EXPECTED_SYMPTOM)


def broadcast_rag_message(task_id, serial_number, topic, anomality_list):
    """
    eda를 통해 메시지를 rag로 broadcast 해주는 함수입니다.
    """
    message = {}

    message["taskId"] = task_id
    message["serialNumber"] = serial_number
    message["product_type"] = "REF"

    symptom_dataset = []
    anomality_number = 0

    print(anomality_list)

    for number, _ in anomality_list:
        anomality_number += 1 << number

    for scenario_index in range(SYMPTOM_NUMBER):
        symptom_number = 0
        for scenario_number in SYMPTOM_CHECK[scenario_index]:
            if anomality_number & scenario_number != 0:
                symptom_number |= scenario_number

        if symptom_number == 0:
            continue

        if scenario_index < HIGH_INTENAL_TEMP_SYMPTOM_INDEX:
            if anomality_number & (1 << INTERNAL_TEMP_INDEX) != 0:
                symptom_number |= 1 << INTERNAL_TEMP_INDEX

        symptom_data = {
            "failure": EXPECTED_SYMPTOM[scenario_index],
            "causes": [],
            "related_sensor": [],
            "event": [],
        }

        for index in range(ANOMALITY_NUMBER):
            if symptom_number & (1 << index) != 0:
                symptom_data["causes"].append(ANOMALITY[index])
                symptom_data["related_sensor"].append(RELATED_SENSOR[index])
                symptom_data["event"] += insert_event(index, anomality_list)

        symptom_dataset.append(symptom_data)

    message["data"] = symptom_dataset

    print(message)

    eda.event_broadcast(topic, message)
