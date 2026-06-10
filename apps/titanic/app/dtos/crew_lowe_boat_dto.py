from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LoweIntroduction:
    """해롤드 로우 (Harold Lowe) 자기소개 유스케이스 출력."""
    id: int
    name: str
