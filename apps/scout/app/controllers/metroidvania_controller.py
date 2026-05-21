from typing import Annotated

from fastapi import APIRouter, Depends

from scout.app.deps import get_metroidvania_controller
from scout.app.schemas.scout_genre_schema import GenreHubSchema
from scout.app.services.metroidvania_service import MetroidvaniaService

router = APIRouter(prefix="/scout/metroidvania", tags=["scout"])


class MetroidvaniaController:
    def __init__(self, service: MetroidvaniaService) -> None:
        self._service = service

    async def get_hub(self) -> GenreHubSchema:
        return await self._service.get_genre_hub()


@router.get("/hub", response_model=GenreHubSchema)
async def get_metroidvania_hub(
    controller: Annotated[MetroidvaniaController, Depends(get_metroidvania_controller)],
) -> GenreHubSchema:
    return await controller.get_hub()
