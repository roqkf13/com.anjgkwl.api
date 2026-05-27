from titanic.app.ports.output.titanic_command_repository import TitanicCommandRepositoryPort
from titanic.domain.entities.titanic import TitanicPassenger

_store: list[TitanicPassenger] = []


class TitanicCommandRepositoryImpl(TitanicCommandRepositoryPort):
    def save(self, passenger: TitanicPassenger) -> None:
        _store.append(passenger)

    def save_many(self, passengers: list[TitanicPassenger]) -> int:
        _store.extend(passengers)
        return len(passengers)
