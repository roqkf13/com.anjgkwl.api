import logging

from scout.app.repositories.metroidvania_repository import MetroidvaniaRepository
from scout.app.schemas.scout_genre_schema import GenreHubSchema

logger = logging.getLogger(__name__)


class MetroidvaniaService:
    def __init__(self, repository: MetroidvaniaRepository) -> None:
        self._repository = repository

    async def get_genre_hub(self) -> GenreHubSchema:
        hub = await self._repository.get_hub()
        logger.info("[MetroidvaniaService] get_genre_hub — id=%s", hub.id)
        return hub
