from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_cal_tester_dto import CalIntroduction
from titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository


class CalTesterPgRepository(CalTesterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, member_id: int, name: str) -> CalIntroduction:
        return CalIntroduction(
            id=member_id * 10000,
            name=f"{name}가 레포지토리에 다녀옴",
        )
