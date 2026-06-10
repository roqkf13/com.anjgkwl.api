from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_walter_roaster_dto import WalterIntroduction
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository


class WalterRoasterPgRepository(WalterRoasterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, member_id: int, name: str) -> WalterIntroduction:
        return WalterIntroduction(
            id=member_id * 10000,
            name=f"{name}가 레포지토리에 다녀옴",
        )
