from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_andrews_architect_dto import AndrewsIntroduction


class IntroduceAndrewsUseCase(ABC):
    """토마스 앤드류스 (Thomas Andrews) 자기소개 유스케이스."""

    @abstractmethod
    async def introduce(self, member_id: int, name: str) -> AndrewsIntroduction:
        ...
