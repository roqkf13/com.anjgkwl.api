from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_smith_captain_dto import SmithIntroduction


class IntroduceSmithUseCase(ABC):
    """스미스 선장 (Captain Edward John Smith) 자기소개 유스케이스."""

    @abstractmethod
    async def introduce(self, member_id: int, name: str) -> SmithIntroduction:
        ...
