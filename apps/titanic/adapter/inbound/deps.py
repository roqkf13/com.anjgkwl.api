from typing import Annotated

from fastapi import Depends

from titanic.adapter.outbound.impl.titanic_command_repository_impl import (
    TitanicCommandRepositoryImpl,
)
from titanic.app.deps import get_jack_service, get_walter_repository
from titanic.app.ports.input.titanic_command import TitanicCommandPort
from titanic.app.ports.input.titanic_query import TitanicQueryPort
from titanic.app.ports.output.titanic_command_repository import TitanicCommandRepositoryPort
from titanic.app.repositories.walter_repository import WalterRepository
from titanic.app.services.jack_service import JackService
from titanic.app.use_cases.titanic_commnad_impl import TitanicCommandImpl
from titanic.app.use_cases.titanic_query_impl import TitanicQueryImpl


def get_titanic_command_repository() -> TitanicCommandRepositoryPort:
    return TitanicCommandRepositoryImpl()


def get_titanic_command(
    repository: Annotated[
        TitanicCommandRepositoryPort, Depends(get_titanic_command_repository)
    ],
) -> TitanicCommandPort:
    return TitanicCommandImpl(repository)


TitanicCommandDep = Annotated[TitanicCommandPort, Depends(get_titanic_command)]


def get_titanic_query(
    walter: Annotated[WalterRepository, Depends(get_walter_repository)],
    jack: Annotated[JackService, Depends(get_jack_service)],
) -> TitanicQueryPort:
    return TitanicQueryImpl(walter, jack)


TitanicQueryDep = Annotated[TitanicQueryPort, Depends(get_titanic_query)]
