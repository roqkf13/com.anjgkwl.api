from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm as PersonOrm
from titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelOrm as BookingOrm
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository


class JackTrainerPgRepository(JackTrainerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_training_data(self) -> list[dict[str, Any]]:
        """생존 예측 모델 학습에 사용할 피처 데이터 조회"""
        rows = (
            await self._session.execute(
                select(PersonOrm, BookingOrm)
                .outerjoin(BookingOrm, BookingOrm.person_id == PersonOrm.id)
                .order_by(PersonOrm.id)
            )
        ).all()
        return [
            {
                "pclass": booking.pclass if booking else None,
                "gender": person.gender,
                "age": person.age,
                "sibsp": person.sib_sp,
                "parch": person.parch,
                "fare": booking.fare if booking else None,
                "survived": person.survived,
            }
            for person, booking in rows
        ]
