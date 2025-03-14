"""
기본 프롬프트 템플릿 모음
"""


class BasePrompts:
    """기본 프롬프트 템플릿을 관리하는 클래스"""

    SYSTEM_DEFAULT = """You are a helpful assistant."""

    RAG_SYSTEM = """You are a helpful assistant. Answer the question based on the given context.
    If the answer cannot be found in the context,
    say "I don't know" instead of making up an answer."""

    DIAGNOSTIC_SYSTEM = (
        DIAGNOSTIC_SYSTEM
    ) = """당신은 가전제품 진단을 전문으로 하는 AI 어시스턴트입니다.
    주어진 제품 고장/비고장 메뉴얼을 기반으로만 응답하며, 만약 충분한 정보가 없으면 '정확한 정보를 제공하기 어렵습니다.'라고 답변하세요.
    항상 존댓말을 사용하며, 아래 JSON 형식을 지켜 주세요:

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

    recommended_solution 필드는 상담사가 보고 고객에게 설명하기 쉽도록 구체적인 원인과 해결 방법이 담긴 메뉴얼을 줄글 형태로 길게 제공해주세요.
    그리고, recommended_solution 필드는 마크다운 형식으로 작성해주세요.

    """

    @staticmethod
    def format_rag_prompt(context, query):
        """RAG 프롬프트 포맷팅 함수"""

        # RAG 결과에서 필요한 데이터 추출
        manuals = context["metadatas"][0]
        distances = context["distances"][0]

        # 벡터 거리 → 심각도 변환 (1 - 거리) * 100%
        severity_scores = [f"{(1 - dist) * 100:.0f}%" for dist in distances]

        # 각 인덱스별 JSON 개별 생성
        structured_manuals = []
        for i, manual in enumerate(manuals):
            structured_manuals.append(
                {
                    "status": "정상",  # 현재 모든 응답이 비고장이므로 기본값 설정
                    "issue": manual["title"],
                    "cause": manual["cause"],
                    "recommended_solution": f"**{manual['title']}**\n\n{manual['solution']}",
                    "severity": severity_scores[i],
                }
            )

        # JSON 문자열 변환
        formatted_context = f"{structured_manuals}"

        return f"""
        제품 고장/비고장 메뉴얼:
        {formatted_context}

        유저의 질문: {query}
        """
