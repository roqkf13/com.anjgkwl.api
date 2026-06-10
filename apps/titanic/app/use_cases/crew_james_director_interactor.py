from __future__ import annotations

from titanic.app.dtos.crew_james_director_dto import (
    DirectorIntroduction,
    ManifestRow,
    UploadManifestResult,
)
from titanic.app.ports.input.crew_james_director_use_case import (
    IntroduceDirectorUseCase,
    UploadTitanicManifestUseCase,
)
from titanic.app.ports.output.crew_james_director_repository import TitanicManifestRepository
from titanic.domain.entities.crew_james_director_entity import ManifestEntry


class UploadTitanicManifestInteractor(UploadTitanicManifestUseCase):
    """원천 행을 도메인 집계로 변환·저장하는 업로드 유스케이스 구현."""

    def __init__(self, repository: TitanicManifestRepository) -> None:
        self._repository = repository

    async def upload(self, rows: list[ManifestRow]) -> UploadManifestResult:
        entries = [
            ManifestEntry.from_raw(
                passenger_id=row.passenger_id,
                name=row.name,
                gender=row.gender,
                sib_sp=row.sib_sp,
                parch=row.parch,
                age=row.age,
                survived=row.survived,
                pclass=row.pclass,
                ticket=row.ticket,
                fare=row.fare,
                cabin=row.cabin,
                embarked=row.embarked,
            )
            for row in rows
        ]
        saved = await self._repository.save_all(entries)
        return UploadManifestResult(saved_count=saved, entries=entries)


class IntroduceDirectorInteractor(IntroduceDirectorUseCase):
    """감독 자기소개 유스케이스 구현(영속성 불필요한 순수 로직)."""

    async def introduce(self, director_id: int, name: str) -> DirectorIntroduction:
        return DirectorIntroduction(
            id=director_id * 10000,
            name=f"{name}가 유스케이스에 다녀옴",
        )
