from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class GenderType(Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class PassengerId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("PassengerId는 빈 값일 수 없습니다.")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class PassengerName:
    full_name: str

    _MAX_LENGTH: ClassVar[int] = 200

    def __post_init__(self) -> None:
        cleaned = (self.full_name or "").strip()
        if not cleaned:
            raise ValueError("Name은 비어 있을 수 없습니다.")
        if len(cleaned) > self._MAX_LENGTH:
            raise ValueError(f"Name은 200자를 초과할 수 없습니다.")
        object.__setattr__(self, "full_name", cleaned)

    @property
    def normalized(self) -> str:
        return self.full_name.strip()


@dataclass(frozen=True, slots=True)
class Gender:
    value: GenderType

    @classmethod
    def from_raw(cls, raw: str | None) -> "Gender":
        if raw is None:
            return cls(GenderType.UNKNOWN)
        normalized = raw.strip().lower()
        if normalized == "male":
            return cls(GenderType.MALE)
        if normalized == "female":
            return cls(GenderType.FEMALE)
        return cls(GenderType.UNKNOWN)

    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE


@dataclass(frozen=True, slots=True)
class Age:
    value: float | None

    _MIN: ClassVar[float] = 0.0
    _MAX: ClassVar[float] = 120.0

    def __post_init__(self) -> None:
        if self.value is not None and not (self._MIN <= self.value <= self._MAX):
            raise ValueError(f"Age는 {self._MIN}~{self._MAX} 범위여야 합니다: {self.value}")

    @classmethod
    def from_raw(cls, raw: str | None) -> "Age":
        if raw is None or raw == "":
            return cls(value=None)
        try:
            return cls(value=float(raw.strip()))
        except ValueError:
            raise ValueError(f"파싱 실패: {raw!r}")

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def is_minor(self) -> bool:
        if self.is_unknown:
            return False
        return self.value < 18.0


@dataclass(frozen=True, slots=True)
class FamilyRelation:
    sib_sp: int
    parch: int

    def __post_init__(self) -> None:
        if self.sib_sp < 0:
            raise ValueError("sib_sp는 음수가 될 수 없습니다.")
        if self.parch < 0:
            raise ValueError("parch는 음수가 될 수 없습니다.")

    @classmethod
    def from_raw(cls, sib_sp: str | None, parch: str | None) -> "FamilyRelation":
        s = int(sib_sp.strip()) if sib_sp else 0
        p = int(parch.strip()) if parch else 0
        return cls(sib_sp=s, parch=p)

    @property
    def total_family_size(self) -> int:
        return self.sib_sp + self.parch

    @property
    def is_alone(self) -> bool:
        return self.total_family_size == 0


@dataclass(frozen=True, slots=True)
class SurvivalStatus:
    survived: bool | None

    @classmethod
    def from_raw(cls, raw: str | None) -> "SurvivalStatus":
        if raw is None or raw == "":
            return cls(survived=None)
        if raw == "1":
            return cls(survived=True)
        if raw == "0":
            return cls(survived=False)
        raise ValueError(f"파싱 실패: {raw!r}")

    @property
    def is_unknown(self) -> bool:
        return self.survived is None
