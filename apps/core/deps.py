"""FastAPI Depends()용 의존성·Annotated 별칭."""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from adapters.db_health_adapter import DatabaseHealthAdapter, get_db_health_adapter
from core.config import Settings, get_settings
from core.database import get_sqlmodel_session
from doro.app.doro_director import DoroDirector
from titanic.app.james_controller import JamesController


def get_james_controller() -> JamesController:
    return JamesController()


def get_doro_director() -> DoroDirector:
    return DoroDirector()


SettingsDep = Annotated[Settings, Depends(get_settings)]

AsyncSessionDep = Annotated[AsyncSession, Depends(get_sqlmodel_session)]
SqlModelSessionDep = AsyncSessionDep

JamesControllerDep = Annotated[JamesController, Depends(get_james_controller)]

DoroDirectorDep = Annotated[DoroDirector, Depends(get_doro_director)]

DatabaseHealthAdapterDep = Annotated[DatabaseHealthAdapter, Depends(get_db_health_adapter)]
