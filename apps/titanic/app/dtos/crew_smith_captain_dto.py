from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SmithIntroduction:
    """스미스 선장 (Captain Edward John Smith) 자기소개 유스케이스 출력."""
    id: int
    name: str
