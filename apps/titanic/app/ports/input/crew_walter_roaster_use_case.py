from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_walter_roaster_dto import WalterIntroduction


class IntroduceWalterUseCase(ABC):
    """Walter Nichols 자기소개 유스케이스."""

    @abstractmethod
    async def introduce(self, member_id: int, name: str) -> WalterIntroduction:
        ...
