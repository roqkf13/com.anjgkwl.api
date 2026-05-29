from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.titanic_model import TitanicRecord
from titanic.app.ports.output.walter_repository import WalterRepository


class WalterPgRepository(WalterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _all_rows(self) -> list[TitanicRecord]:
        result = await self._session.execute(select(TitanicRecord))
        return list(result.scalars().all())

    @staticmethod
    def _to_dict(row: TitanicRecord) -> dict[str, str]:
        return {
            "PassengerId": row.passenger or "",
            "Survived": row.survived or "",
            "Pclass": row.pclass or "",
            "Name": row.name or "",
            "Sex": row.gender or "",
            "Age": row.age or "",
            "SibSp": row.sibsp or "",
            "Parch": row.parch or "",
            "Ticket": row.ticket or "",
            "Fare": row.fare or "",
            "Cabin": row.cabin or "",
            "Embarked": row.embarked or "",
        }

    async def get_data(self) -> list[dict[str, str]]:
        rows = await self._all_rows()
        return [self._to_dict(row) for row in rows]

    async def get_count(self) -> int:
        result = await self._session.execute(
            select(func.count()).select_from(TitanicRecord)
        )
        return result.scalar_one()

    async def get_count_survived(self) -> int:
        rows = await self._all_rows()
        return sum(1 for row in rows if str(row.survived) == "1")

    async def get_count_dead(self) -> int:
        rows = await self._all_rows()
        return sum(1 for row in rows if str(row.survived) == "0")
