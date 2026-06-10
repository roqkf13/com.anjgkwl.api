from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_ruth_validation_dto import RuthIntroduction


class RuthValidationRepository(ABC):
    """루스 드윗 부카터 자기소개 포트."""

    @abstractmethod
    async def introduce_myself(self, member_id: int, name: str) -> RuthIntroduction:
        ...
