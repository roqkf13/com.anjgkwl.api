from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database import get_db
from titanic.adapter.outbound.pg.crew_james_director_pg_repository import JamesDirectorPgRepository
from titanic.app.ports.input.crew_james_director_use_case import (
    IntroduceDirectorUseCase,
    UploadTitanicManifestUseCase,
)
from titanic.app.ports.output.crew_james_director_repository import TitanicManifestRepository
from titanic.app.use_cases.crew_james_director_interactor import (
    IntroduceDirectorInteractor,
    UploadTitanicManifestInteractor,
)


def get_upload_manifest_use_case(
    db: AsyncSession = Depends(get_db),
) -> UploadTitanicManifestUseCase:
    repository: TitanicManifestRepository = JamesDirectorPgRepository(session=db)
    return UploadTitanicManifestInteractor(repository=repository)


def get_introduce_director_use_case() -> IntroduceDirectorUseCase:
    return IntroduceDirectorInteractor()
