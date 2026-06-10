from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_andrews_architect_dto import AndrewsIntroduction


class AndrewsArchitectRepository(ABC):
    """토마스 앤드류스 자기소개 포트."""

    @abstractmethod
    async def introduce_myself(self, member_id: int, name: str) -> AndrewsIntroduction:
        ...
