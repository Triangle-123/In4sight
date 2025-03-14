"""
LLM API의 JSON 문자열 응답으로부터 DTO 객체를 생성하는 모듈
"""

import json
import re
from dataclasses import dataclass
from typing import List


@dataclass
class DiagnosticResult:
    """
    LLM 응답 DTO 객체
    """

    status: str
    issue: List[str]
    cause: List[str]
    recommended_solution: List[str]
    severity: List[str]

    @classmethod
    def from_json(cls, json_str: str) -> List["DiagnosticResult"]:
        """JSON 문자열에서 DiagnosticResult 객체 파싱 (단일 객체 또는 배열 처리)"""
        try:
            json_str = re.sub(
                r"^(```json|\'\'\'|```|\'\'\')|\n(```json|\'\'\'|```|\'\'\')$",
                "",
                json_str,
            )
            data = json.loads(json_str)

            # 배열인 경우 여러 객체 처리
            if isinstance(data, list):
                return [
                    cls(
                        status=item.get("status", ""),
                        issue=(
                            [item.get("issue")]
                            if isinstance(item.get("issue"), str)
                            else item.get("issue", [])
                        ),
                        cause=(
                            [item.get("cause")]
                            if isinstance(item.get("cause"), str)
                            else item.get("cause", [])
                        ),
                        recommended_solution=(
                            [item.get("recommended_solution")]
                            if isinstance(item.get("recommended_solution"), str)
                            else item.get("recommended_solution", [])
                        ),
                        severity=(
                            [item.get("severity")]
                            if isinstance(item.get("severity"), str)
                            else item.get("severity", [])
                        ),
                    )
                    for item in data
                ]

            # 단일 객체인 경우
            return cls(
                status=data.get("status", ""),
                issue=(
                    [data.get("issue")]
                    if isinstance(data.get("issue"), str)
                    else data.get("issue", [])
                ),
                cause=(
                    [data.get("cause")]
                    if isinstance(data.get("cause"), str)
                    else data.get("cause", [])
                ),
                recommended_solution=(
                    [data.get("recommended_solution")]
                    if isinstance(data.get("recommended_solution"), str)
                    else data.get("recommended_solution", [])
                ),
                severity=(
                    [data.get("severity")]
                    if isinstance(data.get("severity"), str)
                    else data.get("severity", [])
                ),
            )
        except json.JSONDecodeError as e:
            raise ValueError("잘못된 JSON 형식입니다") from e
