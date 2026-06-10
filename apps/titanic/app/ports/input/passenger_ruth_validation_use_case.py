from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_ruth_validation_dto import RuthIntroduction


class IntroduceRuthUseCase(ABC):
    """루스 드윗 부카터 (Ruth DeWitt Bukater) 자기소개 유스케이스."""

    @abstractmethod
    async def introduce(self, member_id: int, name: str) -> RuthIntroduction:
        ...
