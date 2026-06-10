from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_ruth_validation_dto import RuthIntroduction
from titanic.app.ports.output.passenger_ruth_validation_repository import RuthValidationRepository


class RuthValidationPgRepository(RuthValidationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, member_id: int, name: str) -> RuthIntroduction:
        return RuthIntroduction(
            id=member_id * 10000,
            name=f"{name}가 레포지토리에 다녀옴",
        )
