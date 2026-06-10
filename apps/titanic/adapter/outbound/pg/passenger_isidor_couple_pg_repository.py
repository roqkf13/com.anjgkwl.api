from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_isidor_couple_dto import IsidorIntroduction
from titanic.app.ports.output.passenger_isidor_couple_repository import IsidorCoupleRepository


class IsidorCouplePgRepository(IsidorCoupleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, member_id: int, name: str) -> IsidorIntroduction:
        return IsidorIntroduction(
            id=member_id * 10000,
            name=f"{name}가 레포지토리에 다녀옴",
        )
