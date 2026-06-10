from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database import create_titanic_tables, get_engine
from titanic.adapter.outbound.mappers.crew_james_director_mapper import JamesDirectorMapper
from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm as PersonOrm
from titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelOrm as BookingOrm
from titanic.app.ports.output.crew_james_director_repository import TitanicManifestRepository
from titanic.domain.entities.crew_james_director_entity import ManifestEntry


class JamesDirectorPgRepository(TitanicManifestRepository):
    """Neon/Postgres 어댑터. ManifestEntry 를 passenger/bookings 두 테이블로 저장한다."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_all(self, entries: list[ManifestEntry]) -> int:
        try:
            return await self._pg_upsert(entries)
        except ProgrammingError:
            # 테이블이 없거나 unique 제약이 없는 구형 스키마 → 드랍 후 재생성
            await self._session.rollback()
            await self._drop_and_recreate()
            return await self._pg_upsert(entries)

    async def _pg_upsert(self, entries: list[ManifestEntry]) -> int:
        # 1. passenger upsert — ON CONFLICT (passenger_id) DO UPDATE
        person_values = [JamesDirectorMapper.to_person_values(e) for e in entries]
        person_stmt = pg_insert(PersonOrm).values(person_values)
        person_stmt = person_stmt.on_conflict_do_update(
            constraint="uq_passenger_passenger_id",
            set_={
                "name": person_stmt.excluded.name,
                "gender": person_stmt.excluded.gender,
                "age": person_stmt.excluded.age,
                "sib_sp": person_stmt.excluded.sib_sp,
                "parch": person_stmt.excluded.parch,
                "survived": person_stmt.excluded.survived,
            },
        ).returning(PersonOrm.id, PersonOrm.passenger_id)

        result = await self._session.execute(person_stmt)
        # passenger_id(타이타닉 ID) → passenger.id(serial PK) 매핑
        pid_to_id = {row.passenger_id: row.id for row in result.fetchall()}

        # 2. bookings upsert — ON CONFLICT (person_id) DO UPDATE
        booking_values = [
            JamesDirectorMapper.to_booking_values(e, pid_to_id[int(e.id.value)])
            for e in entries
        ]
        booking_stmt = pg_insert(BookingOrm).values(booking_values)
        booking_stmt = booking_stmt.on_conflict_do_update(
            constraint="uq_bookings_person_id",
            set_={
                "pclass": booking_stmt.excluded.pclass,
                "ticket": booking_stmt.excluded.ticket,
                "fare": booking_stmt.excluded.fare,
                "cabin": booking_stmt.excluded.cabin,
                "embarked": booking_stmt.excluded.embarked,
            },
        )
        await self._session.execute(booking_stmt)
        await self._session.commit()

        return len(entries)

    async def _drop_and_recreate(self) -> None:
        engine = get_engine()
        if engine is None:
            return
        async with engine.begin() as conn:
            await conn.execute(text("DROP TABLE IF EXISTS bookings CASCADE"))
            await conn.execute(text("DROP TABLE IF EXISTS passenger CASCADE"))
        await create_titanic_tables()
