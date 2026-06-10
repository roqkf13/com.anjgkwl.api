# 예매(Booking) 관련 값 객체.
# 승객 신원 VO(PassengerId·Name·Gender·Age·FamilyComposition·SurvivalStatus)는
# passenger_jack_trainer_vo 를 공유 커널로 재사용하고, 여기서는 예매 정보만 모델링한다.
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


def blank_to_none(raw: Optional[str]) -> Optional[str]:
    """공백/빈 문자열은 '값 없음'으로 정규화한다."""
    if raw is None:
        return None
    cleaned = raw.strip()
    return cleaned or None


class TicketClass(Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3

    @classmethod
    def from_raw(cls, raw: str) -> "TicketClass":
        normalized = raw.strip()
        for member in cls:
            if str(member.value) == normalized:
                return member
        raise ValueError(f"유효하지 않은 객실 등급입니다: {raw!r}")


class Port(Enum):
    """탑승 항구 (Embarked)."""
    CHERBOURG = "C"
    QUEENSTOWN = "Q"
    SOUTHAMPTON = "S"

    @classmethod
    def from_raw(cls, raw: str) -> "Port":
        normalized = raw.strip().upper()
        for member in cls:
            if member.value == normalized:
                return member
        raise ValueError(f"유효하지 않은 탑승 항구입니다: {raw!r}")


@dataclass(frozen=True, slots=True)
class TicketNumber:
    value: str

    def __post_init__(self) -> None:
        cleaned = (self.value or "").strip()
        if not cleaned:
            raise ValueError("티켓 번호는 비어 있을 수 없습니다.")
        object.__setattr__(self, "value", cleaned)


@dataclass(frozen=True, slots=True)
class Fare:
    value: float

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError(f"요금은 음수일 수 없습니다: {self.value}")

    @classmethod
    def from_raw(cls, raw: str) -> "Fare":
        return cls(float(raw.strip()))


@dataclass(frozen=True, slots=True)
class CabinNumber:
    value: str

    def __post_init__(self) -> None:
        cleaned = (self.value or "").strip()
        if not cleaned:
            raise ValueError("객실 번호는 비어 있을 수 없습니다.")
        object.__setattr__(self, "value", cleaned)


@dataclass(frozen=True, slots=True)
class Booking:
    """승객 한 명의 예매 정보를 묶은 값 객체. 누락 가능한 항목은 None 으로 둔다."""
    ticket_class: Optional[TicketClass] = None
    ticket: Optional[TicketNumber] = None
    fare: Optional[Fare] = None
    cabin: Optional[CabinNumber] = None
    port: Optional[Port] = None

    @classmethod
    def from_raw(
        cls,
        *,
        pclass: Optional[str],
        ticket: Optional[str],
        fare: Optional[str],
        cabin: Optional[str],
        embarked: Optional[str],
    ) -> "Booking":
        pclass_raw = blank_to_none(pclass)
        ticket_raw = blank_to_none(ticket)
        fare_raw = blank_to_none(fare)
        cabin_raw = blank_to_none(cabin)
        embarked_raw = blank_to_none(embarked)
        return cls(
            ticket_class=TicketClass.from_raw(pclass_raw) if pclass_raw else None,
            ticket=TicketNumber(ticket_raw) if ticket_raw else None,
            fare=Fare.from_raw(fare_raw) if fare_raw else None,
            cabin=CabinNumber(cabin_raw) if cabin_raw else None,
            port=Port.from_raw(embarked_raw) if embarked_raw else None,
        )
