from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_isidor_couple_dto import IsidorIntroduction


class IsidorCoupleRepository(ABC):
    """이시도르 & 이다 스트라우스 부부 자기소개 포트."""

    @abstractmethod
    async def introduce_myself(self, member_id: int, name: str) -> IsidorIntroduction:
        ...
