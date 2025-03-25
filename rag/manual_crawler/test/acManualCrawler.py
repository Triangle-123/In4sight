import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# 실제 크롤링할 URL (예시 URL, 실제 주소로 변경)
url = "https://downloadcenter.samsung.com/content/PM/202305/20230525172504861/KO/air-web_FAC029-02/content7.html#4605B2F8-DC3E-4EDC-BE73-4B2ABE233835"
response = requests.get(url)
response.encoding = "utf-8"  # 인코딩을 UTF-8로 설정
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# 페이지 내에서 문제(증상)를 나타내는 h4 태그들을 찾습니다.
# (예시로 h4 태그의 클래스 "Heading3-Noline_NoTOC_InContent"를 사용)
h4_tags = soup.find_all(
    "h4", class_=lambda c: c and "Heading3-Noline_NoTOC_InContent" in c
)

# debug
# print("h4 태그 개수: ", len(h4_tags))
# print("h4 태그: ", h4_tags)

data = []
for h4 in h4_tags:
    # 증상은 h4 태그의 텍스트로 사용
    symptom = h4.get_text(strip=True)

    # 다음 형제 요소를 찾습니다.
    next_elem = h4.find_next_sibling()
    # 빈 텍스트 노드 건너뛰기
    while next_elem and not getattr(next_elem, "name", None):
        next_elem = next_elem.find_next_sibling()

    # Case 1: h4 바로 다음 요소가 Description 클래스라면 단일 항목 처리
    if next_elem and next_elem.get("class") and "Description" in next_elem.get("class"):
        cause = "Null"  # 원인 정보가 없으므로 Null 처리
        solution = next_elem.get_text(" ", strip=True)
        data.append({"증상": symptom, "원인": cause, "해결방안": solution})
    else:
        # Case 2: h4 이후부터 다음 h4 태그까지의 형제 요소들을 수집합니다.
        siblings = []
        for sib in h4.find_next_siblings():
            if sib.name == "h4":
                break
            siblings.append(sib)

        # 해당 영역 내에서 원인 태그와 해결방안 태그를 각각 수집합니다.
        cause_cells = [
            elem
            for elem in siblings
            if elem.get("class")
            and (
                "UnorderList_1" in elem.get("class")
                or "UnorderList_1_Cell" in elem.get("class")
            )
        ]
        # "Description_Indent" 또는 "Description" 클래스 둘 다 포함하도록 처리 (필요에 따라 조정)
        solution_divs = [
            elem
            for elem in siblings
            if elem.get("class")
            and (
                "Description_Indent" in elem.get("class")
                or "Description" in elem.get("class")
            )
        ]

        # 두 리스트의 최대 길이 만큼 반복하여 누락 없이 데이터를 저장합니다.
        max_len = max(len(cause_cells), len(solution_divs))
        for i in range(max_len):
            cause_text = (
                cause_cells[i].get_text(" ", strip=True) if i < len(cause_cells) else ""
            )
            solution_text = (
                solution_divs[i].get_text(" ", strip=True)
                if i < len(solution_divs)
                else ""
            )
            data.append(
                {"증상": symptom, "원인": cause_text, "해결방안": solution_text}
            )

# debug
# print("출력 데이터 개수:", len(data))
# print("출력 데이터:", data)

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
    output_filename = os.path.join(
        current_dir, f"{base_filename} ({counter}){extension}"
    )
    counter += 1

df.to_excel(output_filename, index=False)
print(f"엑셀 파일 '{os.path.basename(output_filename)}'이(가) 생성되었습니다.")
