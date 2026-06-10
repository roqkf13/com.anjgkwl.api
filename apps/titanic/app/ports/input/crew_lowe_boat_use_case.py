from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_lowe_boat_dto import LoweIntroduction


class IntroduceLoweUseCase(ABC):
    """해롤드 로우 (Harold Lowe) 자기소개 유스케이스."""

    @abstractmethod
    async def introduce(self, member_id: int, name: str) -> LoweIntroduction:
        ...
