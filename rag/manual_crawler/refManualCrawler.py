import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# 매뉴얼 URL 리스트 (냉장고)
urls = [
    "https://downloadcenter.samsung.com/content/PM/202501/20250103095851140/KO/OID84030_RF9000D_2023_UM_DA68-04789A_KO_Ver34_KO_c6_s1.html",
    "https://downloadcenter.samsung.com/content/PM/202501/20250103095851140/KO/OID84030_RF9000D_2023_UM_DA68-04789A_KO_Ver34_KO_c6_s2.html",
    "https://downloadcenter.samsung.com/content/PM/202501/20250103095851140/KO/OID84030_RF9000D_2023_UM_DA68-04789A_KO_Ver34_KO_c6_s3.html",
    "https://downloadcenter.samsung.com/content/PM/202501/20250103095851140/KO/OID84030_RF9000D_2023_UM_DA68-04789A_KO_Ver34_KO_c6_s4.html",
    "https://downloadcenter.samsung.com/content/PM/202501/20250103095851140/KO/OID84030_RF9000D_2023_UM_DA68-04789A_KO_Ver34_KO_c6_s5.html",
    "https://downloadcenter.samsung.com/content/PM/202501/20250103095851140/KO/OID84030_RF9000D_2023_UM_DA68-04789A_KO_Ver34_KO_c6_s6.html",
    "https://downloadcenter.samsung.com/content/PM/202501/20250103095851140/KO/OID84030_RF9000D_2023_UM_DA68-04789A_KO_Ver34_KO_c6_s7.html",
    "https://downloadcenter.samsung.com/content/PM/202501/20250103095851140/KO/OID84030_RF9000D_2023_UM_DA68-04789A_KO_Ver34_KO_c6_s8.html",
    "https://downloadcenter.samsung.com/content/PM/202501/20250103095851140/KO/OID84030_RF9000D_2023_UM_DA68-04789A_KO_Ver34_KO_c6_s9.html",
]

# 결과를 저장할 리스트
data = []

# URL 요청 및 HTML 파싱
for url in urls:
    response = requests.get(url)
    response.encoding = 'utf-8'  # 인코딩을 UTF-8로 설정
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # main 영역 내부의 section 내에 있는 하위 section들 중 h3 태그가 있는 부분 찾기
    symptom_sections = soup.select("main section section")

    for section in symptom_sections:
        h3 = section.find("h3")
        if h3:
            # 고장/비고장 증상 텍스트 추출
            symptom = h3.get_text(strip=True)
            # 해당 section 내 ul 태그의 li 항목(해결방안) 추출
            ul = section.find("ul")
            if ul:
                # 여러 해결방안 항목이 있다면 줄바꿈으로 구분하여 하나의 문자열로 결합
                # 내부 공백 문자 정규화 - split()으로 모든 공백을 나누고 다시 join하여 정규화된 공백으로 변환
                resolutions = "\n".join(
                    [" ".join(li.get_text().split()) for li in ul.find_all("li")]
                )
            else:
                resolutions = ""

            data.append({"증상": symptom, "해결방안": resolutions})

# 확인을 위해 데이터 프린트
# print(data)

# 데이터프레임 생성: '순번' 컬럼 추가
df = pd.DataFrame(data)
df.insert(0, "순번", range(1, len(df) + 1))

# 결과 엑셀 파일로 저장
current_dir = os.path.dirname(os.path.abspath(__file__))
base_filename = "Solution Lists"
extension = ".xlsx"
output_filename = os.path.join(current_dir, base_filename + extension)
counter = 1

# 파일이 이미 존재하는 경우 번호를 추가
while os.path.exists(output_filename):
    output_filename = os.path.join(current_dir, f"{base_filename}({counter}){extension}")
    counter += 1

df.to_excel(output_filename, index=False)
print(f"엑셀 파일 '{os.path.basename(output_filename)}'이(가) 생성되었습니다.")
