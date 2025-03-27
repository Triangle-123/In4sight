"""
기본 프롬프트 템플릿 모음
"""

import re


class BasePrompts:
    """기본 프롬프트 템플릿을 관리하는 클래스"""

    SYSTEM_DEFAULT = """You are a helpful assistant."""

    RAG_SYSTEM = """You are a helpful assistant. Answer the question based on the given context.
    If the answer cannot be found in the context,
    say "I don't know" instead of making up an answer."""

    DIAGNOSTIC_SYSTEM = """당신은 가전제품 진단을 전문으로 하는 AI 어시스턴트입니다.
        주어진 제품 고장/비고장 매뉴얼을 기반으로만 응답하며, 충분한 정보가 없으면
        "정확한 정보를 제공하기 어렵습니다."라고 답변하세요.
        절대! 임의로 추측해서 답변하면 안 됩니다. 메뉴얼을 기반으로만 응답해주세요.
        항상 존댓말을 사용하며, 아래 JSON 형식을 엄격하게 지켜 주세요:

        [
            {
                "status": "정상" 또는 "주의" 또는 "고장",
                "recommended_solution": "메뉴얼 내용"
            },
            {
                "status": "정상" 또는 "주의" 또는 "고장",
                "recommended_solution": "메뉴얼 내용"
            }
        ]

        아래는 예시입니다. 아래와 같은 형식으로 응답해주세요.
        [
            {
                "status": "주의",
                "recommended_solution": "권장 조치 단계 → 에어컨 전원을 끄고 필터 분리 방법 안내 → 필터 청소 방법 설명 (미지근한 물로 세척 후 완전 건조) → 필터 재장착 방법 안내 → 청소 후 에어컨 재시작 방법 설명"
            }
        ]

        📌 **주의사항**
        1. **각 JSON 객체는 하나의 개별적인 문제 상황을 나타냅니다.**
        → JSON 내부의 필드들이 서로 섞이거나 통합되지 않도록 개별적으로 응답하세요.

        2. **recommended_solution 필드는 상담사가 고객에게 설명하기 쉽도록 작성하세요.**
        - "고객이 이해하기 쉽게" 문장을 구성하세요.
        - recommended_solution필드에 issue는 포함하지 마세요.
        - 해결 방법을 상담사가 고객에게 설명하기 쉽도록 작성하세요.

        3. status 필드는 충분히 고려하여 설정해주세요. 고장이 아닌 경우에 고장으로 반환하면 굉장한 혼란이 올 수 있기 때문입니다.
    """

    @staticmethod
    def format_rag_prompt(context, query, causes, related_sensors):
        """RAG 프롬프트 포맷팅 함수"""

        # 각 문서 블록을 추출하는 패턴
        pattern = r"--- 문서 (\d+) \[(.*?)\] \(유사도: ([\d.]+)\) ---\s*(.*?)(?=(?:--- 문서 \d+)|$)"
        matches = re.findall(pattern, context, re.DOTALL)

        # 메타데이터, 유사도, 문서 내용 추출
        documents = []
        metadatas = []
        distances = []

        for match in matches:
            meta_str = match[1]
            similarity = float(match[2])
            content = match[3].strip()

            # 메타데이터 파싱 - 키:값 쌍으로 구성
            metadata = {}
            # 쉼표로 구분된 키:값 쌍 찾기
            meta_parts = re.findall(r"([^,]+?):\s*([^,]+?)(?:,|$)", meta_str)
            for key, value in meta_parts:
                metadata[key.strip()] = value.strip()

            documents.append(content)
            metadatas.append(metadata)
            distances.append(similarity)

        # JSON 구조를 유지하면서 개별 메뉴얼을 생성
        structured_manuals = []

        for metadata in metadatas:
            # 필요한 키가 있는지 확인
            if any(key in metadata for key in ["response_type", "title", "solution"]):

                manual = {
                    "status": metadata["response_type"],
                    "issue": metadata["title"],
                    "recommended_solution": f"**{metadata['title']}**\n\n{metadata['solution']}",
                }
                structured_manuals.append(manual)

        formatted_context = str(structured_manuals)

        formatted_causes = ""
        for i, cause in enumerate(causes, 1):
            formatted_causes += f"{i}. {cause} \n"

        formatted_sensors = ""
        for related_sensor in related_sensors:
            formatted_sensors.join(related_sensor)

        return f"""
        유저의 증상: {query}
        
        증상에 대한 원인:
        {formatted_causes}
        
        관련 센서: {formatted_sensors}
        제품 고장/비고장 매뉴얼:
        {formatted_context}
        """
