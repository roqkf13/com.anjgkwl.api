from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AndrewsIntroduction:
    """토마스 앤드류스 (Thomas Andrews) 자기소개 유스케이스 출력."""
    id: int
    name: str
