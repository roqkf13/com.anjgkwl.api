from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HartleyIntroduction:
    """왈리스 하틀리 (Wallace Hartley) 자기소개 유스케이스 출력."""
    id: int
    name: str
