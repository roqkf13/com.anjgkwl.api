from __future__ import annotations

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_sqlmodel_session
from titanic.adapter.outbound.pg.james_director_pg_repository import JamesDirectorPgRepository
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.james_director_repository import JamesDirectorRepository
from titanic.app.use_cases.james_director_interactor import JamesDirectorInteractor


def get_james_director_repository(
    db: AsyncSession = Depends(get_sqlmodel_session),
) -> JamesDirectorRepository:
    return JamesDirectorPgRepository(db)


def get_james_director_use_case(
    repository: JamesDirectorRepository = Depends(get_james_director_repository),
) -> JamesDirectorUseCase:
    return JamesDirectorInteractor(repository)
