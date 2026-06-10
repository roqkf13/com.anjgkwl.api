# domain/passenger/value_objects.py
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

    @classmethod
    def from_raw(cls, raw: str) -> "Gender":
        normalized = raw.strip().lower()
        for member in cls:
            if member.value == normalized:
                return member
        raise ValueError(f"유효하지 않은 성별 값입니다: {raw!r}")


class SurvivalStatus(Enum):
    PERISHED = 0
    SURVIVED = 1

    @classmethod
    def from_raw(cls, raw: str) -> "SurvivalStatus":
        normalized = raw.strip()
        if normalized == "1":
            return cls.SURVIVED
        if normalized == "0":
            return cls.PERISHED
        raise ValueError(f"유효하지 않은 생존 값입니다: {raw!r}")

    @property
    def is_survived(self) -> bool:
        return self is SurvivalStatus.SURVIVED


@dataclass(frozen=True, slots=True)
class PassengerId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("PassengerId 는 비어 있을 수 없습니다.")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class Name:
    value: str

    _MAX_LENGTH: ClassVar[int] = 255

    def __post_init__(self) -> None:
        cleaned = (self.value or "").strip()
        if not cleaned:
            raise ValueError("Name 은 비어 있을 수 없습니다.")
        if len(cleaned) > self._MAX_LENGTH:
            raise ValueError("Name 길이가 너무 깁니다.")
        # frozen 이라 직접 대입 불가 → 정규화된 값으로 재설정
        object.__setattr__(self, "value", cleaned)


@dataclass(frozen=True, slots=True)
class Age:
    value: float

    _MIN: ClassVar[float] = 0.0
    _MAX: ClassVar[float] = 120.0

    def __post_init__(self) -> None:
        if not (self._MIN <= self.value <= self._MAX):
            raise ValueError(
                f"Age 는 {self._MIN}~{self._MAX} 범위여야 합니다: {self.value}"
            )

    @classmethod
    def from_raw(cls, raw: str) -> "Age":
        return cls(float(raw.strip()))  # Titanic 데이터는 0.42 같은 소수 존재

    @property
    def is_minor(self) -> bool:
        return self.value < 18.0


@dataclass(frozen=True, slots=True)
class FamilyComposition:
    """sib_sp + parch 를 하나의 개념(동승 가족 구성)으로 묶은 VO."""
    siblings_spouses: int  # sib_sp
    parents_children: int  # parch

    def __post_init__(self) -> None:
        if self.siblings_spouses < 0:
            raise ValueError("sib_sp 는 음수가 될 수 없습니다.")
        if self.parents_children < 0:
            raise ValueError("parch 는 음수가 될 수 없습니다.")

    @classmethod
    def from_raw(cls, sib_sp: str, parch: str) -> "FamilyComposition":
        return cls(int(sib_sp.strip()), int(parch.strip()))

    @property
    def aboard_relatives(self) -> int:
        return self.siblings_spouses + self.parents_children

    @property
    def household_size(self) -> int:
        return self.aboard_relatives + 1  # 본인 포함

    @property
    def is_alone(self) -> bool:
        return self.aboard_relatives == 0