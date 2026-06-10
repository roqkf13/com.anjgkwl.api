from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm as PersonOrm
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository


class SmithCaptainPgRepository(SmithCaptainRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_stats(self) -> dict[str, Any]:
        """전체 승객 생존/사망 통계 조회"""
        total = (
            await self._session.execute(select(func.count()).select_from(PersonOrm))
        ).scalar_one()
        survived = (
            await self._session.execute(
                select(func.count()).where(PersonOrm.survived == 1)
            )
        ).scalar_one()
        return {"total": total, "survived": survived, "perished": total - survived}
