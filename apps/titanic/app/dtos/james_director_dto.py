from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PersonCommand:
    """3NF Person — 식별자·FK 뒤 승객 속성."""

    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass(frozen=True, slots=True, kw_only=True)
class BookingCommand:
    """Booking에 Port(embarked_code, port_name)를 합친 역정규화. country는 제외."""

    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str

