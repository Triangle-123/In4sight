"""
냉장고 냉기 토출구 팬 관련 더미 데이터를 생성하는 모듈입니다.
"""

from datetime import datetime, timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"

# 시작 시간과 종료 시간 설정
start_time = datetime(2024, 3, 1, 0, 0)
end_time = datetime(2024, 3, 3, 0, 0)

# 15분 간격으로 시간 생성
time_range = []
current_time = start_time
while current_time <= end_time:
    time_range.append(current_time)
    current_time += timedelta(minutes=15)

# RPM 데이터 생성
rpm_data = []
for time in time_range:
    # 3월 1일 14:00 ~ 17:00 사이에 과부하 상황 발생
    if datetime(2024, 3, 1, 14, 0) <= time <= datetime(2024, 3, 1, 17, 0):
        # 과부하 상태: 1400 RPM 내외 (표준편차 30)
        rpm = np.random.normal(1400, 30)
    else:
        # 정상 상태: 1200 RPM 내외 (표준편차 20)
        rpm = np.random.normal(1200, 20)

    # rpm = np.random.normal(1200, 20)

    rpm_data.append({"timestamp": time, "fan_rpm": round(rpm, 2)})

# DataFrame 생성 및 CSV 파일로 저장
df = pd.DataFrame(rpm_data)
df.to_csv("fan_rpm_data.csv", index=False)
print("데이터 생성이 완료되었습니다.")
print(f"생성된 데이터 개수: {len(rpm_data)}개")
print("\n데이터 미리보기:")
print(df.head())

# 데이터 시각화
plt.figure(figsize=(15, 7))
plt.plot(df["timestamp"], df["fan_rpm"], "b-", linewidth=1, alpha=0.7)
plt.axhline(y=1200, color="g", linestyle="--", alpha=0.5, label="정상 RPM 기준선")
plt.axhline(y=1400, color="r", linestyle="--", alpha=0.5, label="과부하 RPM 기준선")

# 그래프 스타일 설정
plt.title("냉장고 송풍팬 RPM 변화 추이", fontsize=14, pad=20)
plt.xlabel("시간", fontsize=12)
plt.ylabel("팬 RPM", fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()

# x축 시간 포맷 설정
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H:%M"))
plt.gcf().autofmt_xdate()  # x축 레이블 자동 회전

# y축 범위 설정
plt.ylim(1000, 1600)

# 그래프 저장
plt.tight_layout()
plt.savefig("fan_rpm_graph.png", dpi=300, bbox_inches="tight")
print("\n그래프가 'fan_rpm_graph.png' 파일로 저장되었습니다.")
