"""
LLM API의 JSON 문자열 응답으로부터 DTO 객체를 생성하는 모듈
"""

import json
from dataclasses import dataclass
from typing import List


@dataclass
class DiagnosticResult:
    """
    LLM 응답 DTO 객체
    """

    status: str
    possible_problem: List[str]
    recommended_solution: List[str]
    recommendation_index: List[str]
    description: List[str]

    @classmethod
    def from_json(cls, json_str: str) -> "DiagnosticResult":
        """JSON 문자열에서 DiagnosticResult 객체 파싱"""
        try:
            data = json.loads(json_str)
            return cls(
                status=data.get("status", ""),
                possible_problem=data.get("possible_problem", []),
                recommended_solution=data.get("recommended_solution", []),
                recommendation_index=data.get("recommendation_index", []),
                description=data.get("description", []),
            )
        except json.JSONDecodeError as e:
            raise ValueError("잘못된 JSON 형식입니다") from e
