from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.domain.entities.crew_james_director_entity import ManifestEntry


class TitanicManifestRepository(ABC):
    """명단 집계의 영속성 포트. 도메인 언어(ManifestEntry)로만 대화한다."""

    @abstractmethod
    async def save_all(self, entries: list[ManifestEntry]) -> int:
        """집계 목록을 저장하고 저장된 건수를 반환한다."""
        ...
