from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IsidorIntroduction:
    """이시도르 & 이다 스트라우스 부부 (Isidor & Ida Straus) 자기소개 유스케이스 출력."""
    id: int
    name: str
