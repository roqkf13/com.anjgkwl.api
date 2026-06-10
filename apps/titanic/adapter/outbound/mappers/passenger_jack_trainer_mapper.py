from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm
from titanic.domain.entities.passenger_jack_trainer_entity import Passenger
from titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyComposition,
    Gender,
    Name,
    PassengerId,
    SurvivalStatus,
)


class JackTrainerMapper:
    @staticmethod
    def to_entity(orm: JackTrainerOrm) -> Passenger:
        return Passenger.reconstitute(
            passenger_id=PassengerId(orm.passenger_id or ""),
            name=Name(orm.name or ""),
            gender=Gender.from_raw(orm.gender or "male"),
            family=FamilyComposition.from_raw(
                sib_sp=orm.sib_sp or "0",
                parch=orm.parch or "0",
            ),
            age=Age.from_raw(orm.age) if orm.age else None,
            survival=SurvivalStatus.from_raw(orm.survived) if orm.survived is not None else None,
        )

    @staticmethod
    def to_orm(entity: Passenger) -> JackTrainerOrm:
        return JackTrainerOrm(
            passenger_id=entity.id.value,
            name=entity.name.value,
            gender=entity.gender.value,
            age=str(entity.age.value) if entity.age else None,
            sib_sp=str(entity.family.siblings_spouses),
            parch=str(entity.family.parents_children),
            survived=str(entity.survival.value) if entity.survival else None,
        )
