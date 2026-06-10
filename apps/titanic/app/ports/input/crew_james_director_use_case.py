from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_james_director_dto import (
    DirectorIntroduction,
    ManifestRow,
    UploadManifestResult,
)


class UploadTitanicManifestUseCase(ABC):
    """타이타닉 승객 명단 CSV 업로드 유스케이스."""

    @abstractmethod
    async def upload(self, rows: list[ManifestRow]) -> UploadManifestResult:
        ...


class IntroduceDirectorUseCase(ABC):
    """제임스 카메론 감독 자기소개 유스케이스."""

    @abstractmethod
    async def introduce(self, director_id: int, name: str) -> DirectorIntroduction:
        ...
