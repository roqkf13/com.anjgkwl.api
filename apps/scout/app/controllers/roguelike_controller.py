from typing import Annotated

from fastapi import APIRouter, Depends

from scout.app.deps import get_roguelike_controller
from scout.app.schemas.scout_genre_schema import GenreHubSchema
from scout.app.services.roguelike_service import RoguelikeService

router = APIRouter(prefix="/scout/roguelike", tags=["scout"])


class RoguelikeController:
    def __init__(self, service: RoguelikeService) -> None:
        self._service = service

    async def get_hub(self) -> GenreHubSchema:
        return await self._service.get_genre_hub()


@router.get("/hub", response_model=GenreHubSchema)
async def get_roguelike_hub(
    controller: Annotated[RoguelikeController, Depends(get_roguelike_controller)],
) -> GenreHubSchema:
    return await controller.get_hub()
