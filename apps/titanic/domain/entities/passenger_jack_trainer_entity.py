# domain/passenger/passenger.py
from __future__ import annotations

from .value_objects import (
    PassengerId, Name, Gender, Age, FamilyComposition, SurvivalStatus,
)


class Passenger:
    """Aggregate Root. 동일성은 PassengerId 로만 판단한다."""

    def __init__(
        self,
        passenger_id: PassengerId,
        name: Name,
        gender: Gender,
        family: FamilyComposition,
        age: Age | None = None,
        survival: SurvivalStatus | None = None,
    ) -> None:
        self._id = passenger_id
        self._name = name
        self._gender = gender
        self._family = family
        self._age = age
        self._survival = survival

    # --- 팩토리: 영속성에서 복원할 때 (의도를 이름으로 드러냄) ---
    @classmethod
    def reconstitute(
        cls,
        passenger_id: PassengerId,
        name: Name,
        gender: Gender,
        family: FamilyComposition,
        age: Age | None,
        survival: SurvivalStatus | None,
    ) -> "Passenger":
        return cls(passenger_id, name, gender, family, age, survival)

    # --- 식별자 ---
    @property
    def id(self) -> PassengerId:
        return self._id

    # --- 읽기 전용 노출 (외부에서 상태 직접 변경 불가) ---
    @property
    def name(self) -> Name:
        return self._name

    @property
    def gender(self) -> Gender:
        return self._gender

    @property
    def family(self) -> FamilyComposition:
        return self._family

    @property
    def age(self) -> Age | None:
        return self._age

    @property
    def survival(self) -> SurvivalStatus | None:
        return self._survival

    # --- 도메인 행위 ---
    def record_survival(self, status: SurvivalStatus) -> None:
        """생존 결과 확정. 이미 확정된 값은 변경 불가(불변식 보호)."""
        if self._survival is not None:
            raise ValueError("이미 생존 여부가 확정된 승객입니다.")
        self._survival = status

    @property
    def has_known_age(self) -> bool:
        return self._age is not None

    @property
    def is_survival_known(self) -> bool:
        return self._survival is not None

    # --- 동일성: 값이 아니라 식별자로 비교 ---
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Passenger):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"Passenger(id={self._id.value!r}, name={self._name.value!r})"