from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_andrews_architect_dto import AndrewsIntroduction
from titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository


class AndrewsArchitectPgRepository(AndrewsArchitectRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, member_id: int, name: str) -> AndrewsIntroduction:
        return AndrewsIntroduction(
            id=member_id * 10000,
            name=f"{name}가 레포지토리에 다녀옴",
        )
