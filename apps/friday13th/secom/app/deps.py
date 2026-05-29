from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_sqlmodel_session
from secom.app.repositories.user_repository import UserRepository
from secom.app.services.user_service import UserService


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_sqlmodel_session)],
) -> UserRepository:
    return UserRepository(session)


async def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repository)


async def get_user_controller(
    service: Annotated[UserService, Depends(get_user_service)],
):
    from secom.app.controllers.user_controller import UserController

    return UserController(service)


SqlModelSessionDep = Annotated[AsyncSession, Depends(get_sqlmodel_session)]
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
