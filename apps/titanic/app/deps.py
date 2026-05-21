from typing import Annotated

from fastapi import Depends

from titanic.app.repositories.rose_repository import RoseRepository
from titanic.app.repositories.walter_repository import WalterRepository
from titanic.app.services.jack_service import JackService


def get_walter_repository() -> WalterRepository:
    return WalterRepository()


def get_rose_repository() -> RoseRepository:
    return RoseRepository()


def get_jack_service(
    walter: Annotated[WalterRepository, Depends(get_walter_repository)],
    rose: Annotated[RoseRepository, Depends(get_rose_repository)],
) -> JackService:
    return JackService(walter, rose)


def get_james_controller(
    service: Annotated[JackService, Depends(get_jack_service)],
    reader: Annotated[WalterRepository, Depends(get_walter_repository)],
):
    from titanic.app.controllers.james_controller import JamesController

    return JamesController(service, reader)


WalterRepositoryDep = Annotated[WalterRepository, Depends(get_walter_repository)]
RoseRepositoryDep = Annotated[RoseRepository, Depends(get_rose_repository)]
JackServiceDep = Annotated[JackService, Depends(get_jack_service)]
