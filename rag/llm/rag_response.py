"""
LLM API의 JSON 문자열 응답으로부터 DTO 객체를 생성하는 모듈
"""

import json
import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DiagnosticResult:
    """
    LLM 응답 DTO 객체
    """

    status: str
    recommended_solution: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """객체를 딕셔너리로 변환"""
        return asdict(self)

    def __str__(self) -> str:
        """객체를 문자열로 변환"""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(
        cls, json_str: str
    ) -> Optional[List["DiagnosticResult"] | "DiagnosticResult"]:
        """JSON 문자열에서 DiagnosticResult 객체 파싱 (단일 객체 또는 배열 처리)"""
        try:
            json_str = re.sub(
                r"^(```json|\'\'\'|```|\'\'\')|\n(```json|\'\'\'|```|\'\'\')$",
                "",
                json_str,
            )
            # 문자열인 경우 빈 객체 반환
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError:
                # JSON으로 파싱할 수 없는 문자열인 경우
                return None

            # 배열인 경우 여러 객체 처리
            if isinstance(data, list):
                return [
                    cls(
                        status=item.get("status", ""),
                        recommended_solution=(
                            "".join([item.get("recommended_solution")])
                            if isinstance(item.get("recommended_solution"), str)
                            else item.get("recommended_solution", [])
                        ),
                    )
                    for item in data
                ]

            # 단일 객체인 경우
            return cls(
                status=data.get("status", ""),
                recommended_solution=(
                    [data.get("recommended_solution")]
                    if isinstance(data.get("recommended_solution"), str)
                    else data.get("recommended_solution", [])
                ),
            )
        except json.JSONDecodeError as e:
            raise ValueError("잘못된 JSON 형식입니다") from e
