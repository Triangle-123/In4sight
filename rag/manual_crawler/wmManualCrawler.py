import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


url = "https://downloadcenter.samsung.com/content/PM/202406/20240613175245756/KO/OID63540/OID63540_IB_WF8000CK-AD_BEST_SimpleUX_WF25CB8895_KO_KO_c6_s1.html"

# URL 요청 및 HTML 파싱
response = requests.get(url)
response.encoding = 'utf-8'  # 인코딩을 UTF-8로 설정
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# 모든 table.table.table-bordered 선택 (위치에 상관없이)
tables = soup.select("table.table.table-bordered")

# 각 테이블에서 데이터 추출
data = []
for table in tables:
    tbody = table.find("tbody")
    if tbody is None:
        continue
    rows = tbody.find_all("tr")
    for row in rows:
        tds = row.find_all("td")
        # 최소 두 개의 td가 있어야 증상과 해결방안을 추출
        if len(tds) >= 2:
            # 증상: td > p > strong (없으면 p 또는 td 전체 텍스트로 대체)
            p_tag = tds[0].find("p")
            if p_tag:
                strong_tag = p_tag.find("strong")
                if strong_tag:
                    symptom = strong_tag.get_text(strip=True)
                else:
                    symptom = p_tag.get_text(strip=True)
            else:
                symptom = tds[0].get_text(strip=True)
            
            # 해결방안: td > ul 내의 li 항목을 추출하여 줄바꿈 문자로 결합
            ul_tag = tds[1].find("ul")
            if ul_tag:
                li_items = ul_tag.find_all("li")
                resolution = "\n".join([" ".join(li.get_text().split()) for li in li_items])
            else:
                resolution = " ".join(tds[1].get_text().split())
            
            data.append({"증상": symptom, "해결방안": resolution})

print(data)

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
