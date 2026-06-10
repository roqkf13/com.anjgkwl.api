from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_hartley_violin_dto import HartleyIntroduction
from titanic.app.ports.output.crew_hartley_violin_repository import HartleyViolinRepository


class HartleyViolinPgRepository(HartleyViolinRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, member_id: int, name: str) -> HartleyIntroduction:
        return HartleyIntroduction(
            id=member_id * 10000,
            name=f"{name}가 레포지토리에 다녀옴",
        )
