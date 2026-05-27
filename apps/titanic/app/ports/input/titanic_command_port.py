from typing import Protocol

from titanic.domain.entities.titanic import TitanicPassenger


class TitanicCommandPort(Protocol):
    def register_passenger(self, passenger: TitanicPassenger) -> TitanicPassenger: ...

    def register_passengers(self, passengers: list[TitanicPassenger]) -> int: ...
