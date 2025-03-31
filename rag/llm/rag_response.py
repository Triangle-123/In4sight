"""
LLM API의 JSON 문자열 응답으로부터 DTO 객체를 생성하는 모듈
"""

import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PreviousIssue:
    """과거 상담 이력 정보"""

    date: str
    issue: str
    cause: str
    resolved: bool


@dataclass
class HistoricalContext:
    """고객의 과거 상담 이력 컨텍스트"""

    previous_issues: List[PreviousIssue] = field(default_factory=list)


@dataclass
class PersonalizedSolution:
    """고객 맞춤형 해결책"""

    status: str
    recommended_solution: str
    personalized_context: str = ""


@dataclass
class DiagnosticResult:
    """
    LLM 응답 DTO 객체
    """

    historical_context: HistoricalContext
    personalized_solution: List[PersonalizedSolution]
    preventative_advice: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """객체를 딕셔너리로 변환"""
        return asdict(self)

    def __str__(self) -> str:
        """객체를 문자열로 변환"""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> Optional["DiagnosticResult"]:
        """JSON 문자열에서 DiagnosticResult 객체 파싱"""
        try:
            # 코드 블록 마커 제거
            json_str = re.sub(
                r"^(```json|\'\'\'|```|\'\'\')|\n(```json|\'\'\'|```|\'\'\')$",
                "",
                json_str.strip(),
            )

            # JSON 파싱
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError:
                return None

            # 루트 키가 'result'인 경우 처리
            if isinstance(data, dict) and "result" in data:
                result = data["result"]
            else:
                result = data

            # 과거 상담 이력 파싱
            historical_context_data = result.get("historical_context", {})
            previous_issues = []
            for issue_data in historical_context_data.get("previous_issues", []):
                previous_issues.append(
                    PreviousIssue(
                        date=issue_data.get("date", ""),
                        issue=issue_data.get("issue", ""),
                        cause=issue_data.get("cause", ""),
                        resolved=issue_data.get("resolved", False),
                    )
                )
            historical_context = HistoricalContext(previous_issues=previous_issues)

            # 맞춤형 해결책 파싱
            personalized_solution_data = result.get("personalized_solution", [])
            personalized_solutions = []
            if isinstance(personalized_solution_data, list):
                for solution_data in personalized_solution_data:
                    personalized_solutions.append(
                        PersonalizedSolution(
                            status=solution_data.get("status", ""),
                            recommended_solution=solution_data.get(
                                "recommended_solution", ""
                            ),
                            personalized_context=solution_data.get(
                                "personalized_context", ""
                            ),
                        )
                    )

            # 결과 객체 생성
            return cls(
                historical_context=historical_context,
                personalized_solution=personalized_solutions,
                preventative_advice=result.get("preventative_advice", []),
            )

        except Exception as e:
            raise ValueError(f"JSON 파싱 중 오류 발생: {str(e)}") from e
