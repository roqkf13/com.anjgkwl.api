from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_lowe_boat_dto import LoweIntroduction


class LoweBoatRepository(ABC):
    """해롤드 로우 자기소개 포트."""

    @abstractmethod
    async def introduce_myself(self, member_id: int, name: str) -> LoweIntroduction:
        ...
