from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.pg.crew_lowe_boat_pg_repository import LoweBoatPgRepository
from titanic.app.ports.output.crew_lowe_boat_repository import IoweBoatRepository
from abiswallow.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.crew_lowe_boat_use_case import IoweBoatUseCase
from titanic.app.use_cases.crew_lowe_boat_interactor import IoweBoatInteractor

def get_lowe_boat_use_case(
        db: AsyncSession = Depends(get_db)
) -> IoweBoatUseCase:
    repository: IoweBoatRepository = LoweBoatPgRepository(session=db)
    return IoweBoatInteractor(repository=repository)