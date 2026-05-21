import logging

from scout.app.repositories.roguelike_repository import RoguelikeRepository
from scout.app.schemas.scout_genre_schema import GenreHubSchema

logger = logging.getLogger(__name__)


class RoguelikeService:
    def __init__(self, repository: RoguelikeRepository) -> None:
        self._repository = repository

    async def get_genre_hub(self) -> GenreHubSchema:
        hub = await self._repository.get_hub()
        logger.info("[RoguelikeService] get_genre_hub — id=%s", hub.id)
        return hub
