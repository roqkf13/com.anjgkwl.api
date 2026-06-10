from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CalIntroduction:
    """칼 캘던 하클리 (Caledon Hockley) 자기소개 유스케이스 출력."""
    id: int
    name: str
