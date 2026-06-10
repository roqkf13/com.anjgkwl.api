from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_walter_roaster_dto import WalterIntroduction


class WalterRoasterRepository(ABC):
    """Walter Nichols 자기소개 포트."""

    @abstractmethod
    async def introduce_myself(self, member_id: int, name: str) -> WalterIntroduction:
        pass
