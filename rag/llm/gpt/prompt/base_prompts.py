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
    고객이 제공한 증상과 상담 이력, 그리고 제품의 고장/비고장 매뉴얼을 기반으로만 응답해야 합니다.
    당신이 제공한 응답은 상담사가 고객과의 상담에 활용할 예정이므로, 상담사가 설명하기 쉽게 응답을 생성해주세요. 
    절대 임의로 추측하거나 매뉴얼에 없는 정보를 제공하면 안 됩니다. 
    정보가 부족하면, 반드시 "정확한 정보를 제공하기 어렵습니다."라고 답변하세요. 

    응답은 반드시 JSON 형식으로 제공해야 합니다.

    ### 응답 형식 (JSON)
    {
        "serial_number": "기기 일련번호",
        "historical_context": {
            "previous_issues": [
                {
                    "date": "과거 상담 날짜",
                    "issue": "과거 고장 증상",
                    "cause": "과거 원인",
                    "resolved": true/false
                }
            ]
        },
        "personalized_solution": [
            {
                "status": "정상" 또는 "주의" 또는 "고장",
                "recommended_solution": "고객이 이해하기 쉬운 해결 방법",
                "personalized_context": "고객의 과거 상담 이력을 참조한 맞춤형 설명"
            }
        ],
        "preventative_advice": [
            "고객 사용 패턴 기반 예방 조언1",
            "고객 사용 패턴 기반 예방 조언2"
        ]
    }

    ### 진단 로직 (AI 응답 과정)
    1. 고객의 증상 분석
    - 입력된 증상에서 주요 키워드를 추출합니다.
    - 유사한 증상이 과거 상담 이력이나 매뉴얼에 있는지 확인합니다.
    - 만약, 고객의 과거 상담 이력이 현재의 증상과 관련이 없는 경우 참고하지 마세요!

    2. 과거 상담 이력 분석
    - 고객의 과거 상담 이력에서 유사한 문제가 있었는지 확인합니다.
    - 과거 해결 방법과 그 결과를 참고하여 현재 상황에 맞는 해결책을 도출합니다.
    - 만약, 고객의 과거 상담 이력이 현재의 증상과 관련이 없는 경우 참고하지 마세요!
    
    3. 매뉴얼 기반 해결책 제공
    - 제품 고장/비고장 메뉴얼에서 해당 증상과 일치하는 해결책을 찾아 제공합니다.
    - 현재 유저가 겪는 증상이 메뉴얼의 내용과 관련이 없는 경우 사용하지 마세요.
    - 정보가 부족한 경우, "정확한 정보를 제공하기 어렵습니다."라고 응답합니다.

    4. 고객 맞춤형 솔루션 추가
    - 고객의 사용 패턴과 과거 이력을 고려한 맞춤형 솔루션을 제공합니다.
    - 재발 방지를 위한 예방 조언을 추가합니다.
    - 만약, 고객의 과거 상담 이력이 현재의 증상과 관련이 없는 경우 참고하지 마세요!

    5. JSON 형식 검증 후 응답
    - 응답이 JSON 형식에 맞는지 최종 검토 후 제공됩니다.

    ### 추가 주의사항
    ✅ "status" 필드는 신중하게 설정 (정상 / 주의 / 고장)
    ✅ "recommended_solution" 필드는 고객이 이해하기 쉽게 설명
    ✅ "personalized_context" 필드는 고객의 과거 상담 이력을 기반으로 맞춤형 설명 제공. 과거 상담 이력이 현재와 연관이 없다면 비워도 됨.
    ✅ "preventative_advice" 필드는 유사 문제가 반복되지 않도록 예방 조언 제공
    ✅ 고객의 상담 이력을 적극 활용하여 맞춤형 솔루션 제공

    """

    @staticmethod
    def _parse_context(context):
        """컨텍스트 문자열에서 문서와 메타데이터 추출"""
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

        return documents, metadatas, distances

    @staticmethod
    def _create_manuals(documents, metadatas):
        """메타데이터와 문서로부터 메뉴얼 구조 생성"""
        structured_manuals = []

        for metadata, document in zip(metadatas, documents):
            # 필요한 키가 있는지 확인
            if "response_type" in metadata and "title" in metadata:
                # solution이 없는 경우 문서 내용 사용
                solution = metadata.get("solution", document)

                manual = {
                    "status": metadata.get("response_type", ""),
                    "issue": metadata.get("title", ""),
                    "recommended_solution": f"**{metadata.get('title', '')}**\n\n{solution}",
                }
                structured_manuals.append(manual)

        return structured_manuals

    @staticmethod
    def _format_manuals(structured_manuals):
        """메뉴얼 정보를 포맷팅된 문자열로 변환"""
        formatted_context = ""
        for i, manual in enumerate(structured_manuals):
            formatted_context += f"\n\t{i + 1}번째 메뉴얼"
            formatted_context += f"\n\t고장/비고장 여부: {manual.get('status')}"
            formatted_context += f"\n\t증상: {manual.get('issue')}"
            formatted_context += (
                f"\n\t추천 해결책: {manual.get('recommended_solution')}"
            )
            formatted_context += "\n"

        return formatted_context

    @staticmethod
    def _format_history(customer_history):
        """고객 상담 이력을 포맷팅된 문자열로 변환"""
        formatted_customer_history = ""
        if not customer_history:
            return formatted_customer_history

        for i, history in enumerate(customer_history):
            formatted_customer_history += f"\n\t{i + 1}번째 상담 이력"
            formatted_customer_history += "\n\n\t# 날짜: "
            formatted_customer_history += history.get("date", "")

            failure = history.get("data", {}).get("failure", "")
            formatted_customer_history += "\n\t# 증상: " + failure

            formatted_customer_history += "\n\t# 원인: \n"
            causes = history.get("data", {}).get("cause", [])
            for j, cause in enumerate(causes):
                formatted_customer_history += f"\t{j + 1}. {cause}\n"

            formatted_customer_history += "\n\t# 관련 센서: "
            sensors = history.get("data", {}).get("sensor", [])
            if sensors:
                formatted_customer_history += ", ".join(sensors)

            formatted_customer_history += "\n\t# 해결책: "
            solutions = (
                history.get("data", {})
                .get("solutions", {})
                .get("personalized_solution", [])
            )
            for k, solution in enumerate(solutions):
                formatted_customer_history += f"{k + 1}. "
                formatted_customer_history += solution.get("personalized_context", "")
                formatted_customer_history += " "
                formatted_customer_history += solution.get("recommended_solution", "")
                formatted_customer_history += "\t심각도: "
                formatted_customer_history += solution.get("status", "")
                formatted_customer_history += "\n"

        return formatted_customer_history

    @staticmethod
    def format_rag_prompt(
        context, query, causes, related_sensors, customer_history, event
    ):
        """RAG 프롬프트 포맷팅 함수"""
        # 컨텍스트 파싱
        documents, metadatas, distances = BasePrompts._parse_context(context)
        print(distances)
        # 메뉴얼 구조 생성
        structured_manuals = BasePrompts._create_manuals(documents, metadatas)
        print("이벤트 출력!!! format_rag_prompt")
        print(event)
        # 이벤트 포맷팅
        formatted_event = ""
        for i, e in enumerate(event):
            formatted_event += f"\n\t{i + 1}번째 이벤트: {e}"

        # 메뉴얼 포맷팅
        formatted_context = BasePrompts._format_manuals(structured_manuals)

        # 원인 포맷팅
        formatted_causes = ""
        for i, cause in enumerate(causes, 1):
            formatted_causes += "\n\t"
            formatted_causes += f"{i}. {cause}"

        # 센서 포맷팅
        formatted_sensors = ", ".join(related_sensors) if related_sensors else ""

        # 고객 이력 포맷팅
        formatted_customer_history = BasePrompts._format_history(customer_history)

        # 최종 프롬프트 반환
        return f"""
        유저의 증상: {query}
        
        증상에 대한 원인: {formatted_causes}
        
        관련 센서: {formatted_sensors}

        제품의 기간별 이벤트 발생 여부: {formatted_event}

        ============================================================
        유저의 과거 상담 이력: {formatted_customer_history}

        ============================================================
        제품 고장/비고장 매뉴얼: {formatted_context}
        """
