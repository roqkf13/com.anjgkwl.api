from __future__ import annotations

from fastapi import APIRouter

from titanic.adapter.inbound.deps import WalterQueryDep

router = APIRouter(prefix="/titanic", tags=["walter"])


@router.get("/data")
async def read_titanic_data(query: WalterQueryDep):
    df = await query.get_titanic_data()
    return df.to_dict(orient="records")


@router.get("/count")
async def read_titanic_count(query: WalterQueryDep):
    return {"count": await query.get_titanic_data_count()}


@router.get("/count/survived")
async def read_titanic_count_survived(query: WalterQueryDep):
    return {"count": await query.get_titanic_data_count_survived()}


@router.get("/count/dead")
async def read_titanic_count_dead(query: WalterQueryDep):
    return {"count": await query.get_titanic_data_count_dead()}
