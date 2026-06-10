from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_hartley_violin_dto import HartleyIntroduction


class IntroduceHartleyUseCase(ABC):
    """왈리스 하틀리 (Wallace Hartley) 자기소개 유스케이스."""

    @abstractmethod
    async def introduce(self, member_id: int, name: str) -> HartleyIntroduction:
        ...
