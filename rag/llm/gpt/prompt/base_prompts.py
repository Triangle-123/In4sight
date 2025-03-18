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
        항상 존댓말을 사용하며, 아래 JSON 형식을 엄격하게 지켜 주세요:

        [
            {
                "status": "정상" 또는 "고장",
                "issue": "문제 상황",
                "cause": "문제 원인",
                "recommended_solution": "메뉴얼 내용 (마크다운 형식)",
                "severity": "심각도%"
            },
            {
                "status": "정상" 또는 "고장",
                "issue": "문제 상황",
                "cause": "문제 원인",
                "recommended_solution": "메뉴얼 내용 (마크다운 형식)",
                "severity": "심각도%"
            }
        ]

        📌 **주의사항**
        1. **각 JSON 객체는 하나의 개별적인 문제 상황을 나타냅니다.**
        → JSON 내부의 필드들이 서로 섞이거나 통합되지 않도록 개별적으로 응답하세요.

        2. **recommended_solution 필드는 상담사가 고객에게 설명하기 쉽도록 작성하세요.**
        - "고객이 이해하기 쉽게" 문장을 구성하세요.
        - recommended_solution필드에 issue는 포함하지 마세요.
        - 해결 방법을 단계별로 제시하세요.
        - 만약 해결 방법의 단계가 여러 단계일 경우 1️⃣과 같은 이모지를 사용하여 예쁘게 작성하세요.
        - 예시:
            ```markdown
            1️⃣ 냉장고 문을 열고 닫을 때의 소리를 주의 깊게 들어보세요.
            2️⃣ 만약 일정 시간이 지나도 지속되면, 제품 설치 환경을 확인하세요.
            ```

        3. **severity는 벡터 거리 기반 심각도 값을 의미합니다.**
        - 0%에 가까울수록 문제 발생 가능성이 낮음
        - 100%에 가까울수록 고장 가능성이 높음
        - status가 정상일 경우 0%에 가까워야 합니다.

        4. **cause는 문제 상황에 대한 원인을 의미합니다.**
        - 상담사가 한 번에 이해할 수 있도록 쉽게 문장을 구성하세요
        - 예시:
            ```markdown
            냉장고에서 '쉭~' 또는 '뚜둑' 하는 소리가 나는 경우,
            내부 압력 변화로 인해 발생할 수 있습니다.
            ```
    """

    @staticmethod
    def format_rag_prompt(context, query):
        """RAG 프롬프트 포맷팅 함수"""
        # 정규식을 사용하여 문서 정보를 추출

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
        # 벡터 거리 → 심각도 변환 (1 - 거리) * 100%
        severity_scores = [f"{(1 - dist) * 100:.0f}%" for dist in distances]

        # JSON 구조를 유지하면서 개별 메뉴얼을 생성
        structured_manuals = []
        for i, metadata in enumerate(metadatas):
            # 필요한 키가 있는지 확인
            if all(
                key in metadata
                for key in ["response_type", "title", "cause", "solution"]
            ):
                manual = {
                    "status": metadata["response_type"],
                    "issue": metadata["title"],
                    "cause": metadata["cause"],
                    "recommended_solution": f"**{metadata['title']}**\n\n{metadata['solution']}",
                    "severity": severity_scores[i],
                }
                structured_manuals.append(manual)

        formatted_context = str(structured_manuals)

        return f"""
        제품 고장/비고장 매뉴얼:
        {formatted_context}
        
        유저의 질문: {query}
        """
