from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_sqlmodel_session
from titanic.adapter.outbound.pg.walter_pg_reopsitory import WalterPgRepository
from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.ports.output.walter_repository import WalterRepository
from titanic.app.use_cases.walter_query import WalterQuery

router = APIRouter(prefix="/titanic", tags=["walter"])


def _walter_use_case(db: AsyncSession) -> WalterUseCase:
    repository: WalterRepository = WalterPgRepository(db)
    return WalterQuery(repository)


@router.get("/data")
async def read_titanic_data(db: AsyncSession = Depends(get_sqlmodel_session)):
    use_case = _walter_use_case(db)
    df = await use_case.get_titanic_data()
    return df.to_dict(orient="records")


@router.get("/count")
async def read_titanic_count(db: AsyncSession = Depends(get_sqlmodel_session)):
    use_case = _walter_use_case(db)
    return {"count": await use_case.get_titanic_data_count()}


@router.get("/count/survived")
async def read_titanic_count_survived(db: AsyncSession = Depends(get_sqlmodel_session)):
    use_case = _walter_use_case(db)
    return {"count": await use_case.get_titanic_data_count_survived()}


@router.get("/count/dead")
async def read_titanic_count_dead(db: AsyncSession = Depends(get_sqlmodel_session)):
    use_case = _walter_use_case(db)
    return {"count": await use_case.get_titanic_data_count_dead()}
