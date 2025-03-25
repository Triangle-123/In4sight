"""
냉장고 적재량 관련 이상치를 판단하는 모듈입니다.
"""

LIMIT_OPEN_NUMBER = 50
LIMIT_MAX_INTERVAL = 20 * 60 * 10**9  # 20분을 나노초로 환산


def check_loading_rate_anormality(df_event, anormality_list, related_sensor):
    """
    냉장고 적재량 이상치를 판단하는 로직입니다.
    """
    # 85% 이상인 데이터의 인덱스 찾기
    high_load_indices = df_event[df_event["load_percent"] >= 85].index

    if len(high_load_indices) == 0:
        return

    # 연속된 인덱스 그룹화
    chunks = []
    current_chunk = [high_load_indices[0]]

    for i in range(1, len(high_load_indices)):
        if high_load_indices[i] - high_load_indices[i - 1] == 1:
            current_chunk.append(high_load_indices[i])
        else:
            chunks.append(current_chunk)
            current_chunk = [high_load_indices[i]]

    chunks.append(current_chunk)

    # 각 청크 처리
    for chunk in chunks:
        start_time = df_event.iloc[chunk[0]]["_time"]
        end_time = df_event.iloc[chunk[-1]]["_time"]
        load_values = df_event.iloc[chunk]["load_percent"].tolist()

        days, hours = divmod((end_time - start_time).seconds, 86400)
        hours, minutes = divmod(hours, 3600)
        minutes //= 60

        # 시간 정보를 담을 리스트 생성
        time_parts = []

        # 0이 아닌 값만 리스트에 추가
        if days > 0:
            time_parts.append(f"{days}일")
        if hours > 0:
            time_parts.append(f"{hours}시간")
        if minutes > 0:
            time_parts.append(f"{minutes}분")

        # 리스트의 요소들을 공백으로 연결
        time_str = " ".join(time_parts)

        date_str = f"{start_time.date().year}년 {start_time.date().month}월 {start_time.date().day}일"

        if time_str == "":
            anormality_list.append(
                f"{date_str}에 {len(load_values)}건의 과다 적재가 발생했습니다."
            )
        else:
            anormality_list.append(
                f"{date_str}일부터 총 {time_str} 동안 {len(load_values)}건의 과다 적재가 발생했습니다."
            )

        related_sensor.append("적재량")
