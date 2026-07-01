from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from sherlock_homes.adapter.outbound.orm.received_email_orm import ReceivedEmailOrm
from sherlock_homes.app.dtos.received_email_dto import ReceivedEmailCommand, ReceivedEmailListResult, ReceivedEmailResult
from sherlock_homes.app.ports.output.received_email_repository import ReceivedEmailRepository


class ReceivedEmailDbRepository(ReceivedEmailRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, command: ReceivedEmailCommand) -> ReceivedEmailResult:
        stmt = (
            pg_insert(ReceivedEmailOrm)
            .values(
                id=str(uuid.uuid4()),
                gmail_id=command.gmail_id,
                thread_id=command.thread_id,
                from_address=command.from_,
                to=command.to,
                subject=command.subject,
                snippet=command.snippet,
            )
            .on_conflict_do_update(
                index_elements=["gmail_id"],
                set_={
                    "thread_id": command.thread_id,
                    "from_address": command.from_,
                    "to": command.to,
                    "subject": command.subject,
                    "snippet": command.snippet,
                },
            )
            .returning(ReceivedEmailOrm)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        row = result.scalar_one()
        return self._to_result(row)

    async def list_all(self) -> ReceivedEmailListResult:
        rows = (await self._session.execute(select(ReceivedEmailOrm))).scalars().all()
        return ReceivedEmailListResult(
            total=len(rows),
            emails=[self._to_result(r) for r in rows],
        )

    @staticmethod
    def _to_result(row: ReceivedEmailOrm) -> ReceivedEmailResult:
        return ReceivedEmailResult(
            id=row.id,
            gmail_id=row.gmail_id,
            thread_id=row.thread_id,
            from_=row.from_,
            to=row.to,
            subject=row.subject,
            snippet=row.snippet,
        )
