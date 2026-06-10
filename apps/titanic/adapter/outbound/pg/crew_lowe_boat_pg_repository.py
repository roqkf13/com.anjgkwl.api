from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_lowe_boat_dto import LoweIntroduction
from titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository


class LoweBoatPgRepository(LoweBoatRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, member_id: int, name: str) -> LoweIntroduction:
        return LoweIntroduction(
            id=member_id * 10000,
            name=f"{name}가 레포지토리에 다녀옴",
        )
