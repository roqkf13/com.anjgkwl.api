import logging

from scout.app.repositories.openworld_repository import OpenworldRepository
from scout.app.schemas.scout_genre_schema import GenreHubSchema

logger = logging.getLogger(__name__)


class OpenworldService:
    def __init__(self, repository: OpenworldRepository) -> None:
        self._repository = repository

    async def get_genre_hub(self) -> GenreHubSchema:
        hub = await self._repository.get_hub()
        logger.info("[OpenworldService] get_genre_hub — id=%s", hub.id)
        return hub
