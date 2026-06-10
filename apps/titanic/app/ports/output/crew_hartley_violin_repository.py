from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_hartley_violin_dto import HartleyIntroduction


class HartleyViolinRepository(ABC):
    """왈리스 하틀리 자기소개 포트."""

    @abstractmethod
    async def introduce_myself(self, member_id: int, name: str) -> HartleyIntroduction:
        ...
