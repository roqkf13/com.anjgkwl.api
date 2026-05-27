from titanic.app.ports.input.titanic_command import TitanicCommandPort
from titanic.app.ports.output.titanic_command_repository import TitanicCommandRepositoryPort
from titanic.domain.entities.titanic import TitanicPassenger


class TitanicCommandImpl(TitanicCommandPort):
    def __init__(self, repository: TitanicCommandRepositoryPort) -> None:
        self._repository = repository

    def register_passenger(self, passenger: TitanicPassenger) -> TitanicPassenger:
        self._repository.save(passenger)
        return passenger

    def register_passengers(self, passengers: list[TitanicPassenger]) -> int:
        return self._repository.save_many(passengers)
