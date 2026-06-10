from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoseIntroduction:
    """로즈 드윗 부카터 (Rose DeWitt Bukater) 자기소개 유스케이스 출력."""
    id: int
    name: str
