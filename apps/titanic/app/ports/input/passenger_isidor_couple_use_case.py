from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_isidor_couple_dto import IsidorIntroduction


class IntroduceIsidorUseCase(ABC):
    """이시도르 & 이다 스트라우스 부부 (Isidor & Ida Straus) 자기소개 유스케이스."""

    @abstractmethod
    async def introduce(self, member_id: int, name: str) -> IsidorIntroduction:
        ...
