"""
냉장고 적재량 관련 이상치를 판단하는 모듈입니다.
"""

import logging

# from datetime import timedelta

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y/%m/%d %I:%M:%S%p",
    level=logging.INFO,
)


def check_loading_rate_anormality(df_event, anormality_list, related_sensor):
    """
    냉장고 적재량 이상치를 판단하는 로직입니다.
    """
    high_load_indices = df_event[df_event["load_percent"] >= 85].index

    logging.debug("[적재량 검사] 전체 데이터 수: %d", len(df_event))
    logging.debug("[적재량 검사] 과다 적재 인덱스 수: %d", len(high_load_indices))

    # if len(high_load_indices) == 0:
    #     logging.info("[적재량 정상] 과다 적재 없음.")
    #     return

    # # 연속된 인덱스 그룹화
    # chunks = []
    # current_chunk = [high_load_indices[0]]

    # for i in range(1, len(high_load_indices)):
    #     if high_load_indices[i] - high_load_indices[i - 1] == 1:
    #         current_chunk.append(high_load_indices[i])
    #     else:
    #         chunks.append(current_chunk)
    #         current_chunk = [high_load_indices[i]]

    # chunks.append(current_chunk)

    # logging.info("[적재량 검사] 과다 적재 연속 구간 수: %d", len(chunks))

    # # 각 청크 처리
    # for chunk in chunks:
    #     start_time = df_event.iloc[chunk[0]]["_time"] + timedelta(hours=9)
    #     end_time = df_event.iloc[chunk[-1]]["_time"] + timedelta(hours=9)
    #     load_values = df_event.iloc[chunk]["load_percent"].tolist()

    #     logging.debug(
    #         "[적재량 구간] 시작: %s, 종료: %s, 값 개수: %d",
    #         start_time,
    #         end_time,
    #         len(load_values),
    #     )

    #     duration = end_time - start_time
    #     total_minutes = duration.total_seconds() / 60
    #     days = int(total_minutes // 1440)
    #     hours = int((total_minutes % 1440) // 60)
    #     minutes = int(total_minutes % 60)

    #     time_parts = []
    #     if days > 0:
    #         time_parts.append(f"{days}일")
    #     if hours > 0:
    #         time_parts.append(f"{hours}시간")
    #     if minutes > 0:
    #         time_parts.append(f"{minutes}분")

    #     time_str = " ".join(time_parts)
    #     date_str = f"{start_time.year}년 {start_time.month}월 {start_time.day}일"

    #     if time_str == "":
    #         msg = f"{date_str}에 {len(load_values)}건의 과다 적재가 발생했습니다."
    #     else:
    #         msg = f"{date_str}부터 총 {time_str} 동안 {len(load_values)}건의 과다 적재가 발생했습니다."

    #     anormality_list.append(msg)
    #     related_sensor.append("적재량")

    #     logging.info("[과다 적재 감지] %s", msg)

    if len(high_load_indices) > 0:
        anormality_list.append(4)
        related_sensor.append("적재량")
