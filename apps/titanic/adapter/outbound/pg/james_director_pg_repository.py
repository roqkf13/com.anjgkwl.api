from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.titanic_model import TitanicRecord
from titanic.app.ports.output.james_director_repository import JamesDirectorRepository


class JamesDirectorPgRepository(JamesDirectorRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_all(self, records: list[dict[str, Any]]) -> int:
        objects = [TitanicRecord(**record) for record in records]
        self._session.add_all(objects)
        await self._session.commit()
        return len(objects)

    async def list_paginated(
        self, page: int, page_size: int
    ) -> tuple[int, list[dict[str, Any]]]:
        total_result = await self._session.execute(
            select(func.count()).select_from(TitanicRecord)
        )
        total = total_result.scalar_one()

        rows_result = await self._session.execute(
            select(TitanicRecord)
            .order_by(TitanicRecord.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        rows = rows_result.scalars().all()

        items = [
            {
                "id": row.id,
                "passenger_id": row.passenger_id,
                "survived": row.survived,
                "pclass": row.pclass,
                "name": row.name,
                "gender": row.gender,
                "age": row.age,
                "sib_sp": row.sib_sp,
                "parch": row.parch,
                "ticket": row.ticket,
                "fare": row.fare,
                "cabin": row.cabin,
                "embarked": row.embarked,
            }
            for row in rows
        ]
        return total, items
