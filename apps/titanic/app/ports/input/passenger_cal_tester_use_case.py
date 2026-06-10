from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_cal_tester_dto import CalIntroduction


class IntroduceCalUseCase(ABC):
    """칼 캘던 하클리 (Caledon Hockley) 자기소개 유스케이스."""

    @abstractmethod
    async def introduce(self, member_id: int, name: str) -> CalIntroduction:
        ...
