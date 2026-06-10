from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_rose_model_dto import RoseIntroduction


class IntroduceRoseUseCase(ABC):
    """로즈 드윗 부카터 (Rose DeWitt Bukater) 자기소개 유스케이스."""

    @abstractmethod
    async def introduce(self, member_id: int, name: str) -> RoseIntroduction:
        ...
