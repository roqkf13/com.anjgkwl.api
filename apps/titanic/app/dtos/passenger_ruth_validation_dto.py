from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuthIntroduction:
    """루스 드윗 부카터 (Ruth DeWitt Bukater) 자기소개 유스케이스 출력."""
    id: int
    name: str
