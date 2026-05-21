import logging

from scout.app.repositories.soulslike_repository import SoulslikeRepository
from scout.app.schemas.scout_genre_schema import GenreHubSchema

logger = logging.getLogger(__name__)


class SoulslikeService:
    def __init__(self, repository: SoulslikeRepository) -> None:
        self._repository = repository

    async def get_genre_hub(self) -> GenreHubSchema:
        hub = await self._repository.get_hub()
        logger.info("[SoulslikeService] get_genre_hub — id=%s", hub.id)
        return hub
