from typing import Annotated

from fastapi import APIRouter, Depends

from scout.app.deps import get_soulslike_controller
from scout.app.schemas.scout_genre_schema import GenreHubSchema
from scout.app.services.soulslike_service import SoulslikeService

router = APIRouter(prefix="/scout/soulslike", tags=["scout"])


class SoulslikeController:
    def __init__(self, service: SoulslikeService) -> None:
        self._service = service

    async def get_hub(self) -> GenreHubSchema:
        return await self._service.get_genre_hub()


@router.get("/hub", response_model=GenreHubSchema)
async def get_soulslike_hub(
    controller: Annotated[SoulslikeController, Depends(get_soulslike_controller)],
) -> GenreHubSchema:
    return await controller.get_hub()
