from typing import Annotated

from fastapi import APIRouter, Depends

from scout.app.deps import get_openworld_controller
from scout.app.schemas.scout_genre_schema import GenreHubSchema
from scout.app.services.openworld_service import OpenworldService

router = APIRouter(prefix="/scout/openworld", tags=["scout"])


class OpenworldController:
    def __init__(self, service: OpenworldService) -> None:
        self._service = service

    async def get_hub(self) -> GenreHubSchema:
        return await self._service.get_genre_hub()


@router.get("/hub", response_model=GenreHubSchema)
async def get_openworld_hub(
    controller: Annotated[OpenworldController, Depends(get_openworld_controller)],
) -> GenreHubSchema:
    return await controller.get_hub()
