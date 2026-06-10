from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_cal_tester_dto import CalIntroduction


class CalTesterRepository(ABC):
    """칼 캘던 하클리 자기소개 포트."""

    @abstractmethod
    async def introduce_myself(self, member_id: int, name: str) -> CalIntroduction:
        ...
