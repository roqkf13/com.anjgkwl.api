import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from scout.app.deps import get_scout_director_controller

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/scout", tags=["scout"])


class ScoutDirectorStatus(BaseModel):
    module: str
    message: str


class ScoutDirectorController:
    """Scout 상위 조율용 컨트롤러 (기존 scout_director 역할)."""

    async def status(self) -> ScoutDirectorStatus:
        logger.info("[ScoutDirectorController] status")
        return ScoutDirectorStatus(module="scout", message="Scout director is ready.")


@router.get("/status", response_model=ScoutDirectorStatus)
async def get_scout_status(
    controller: Annotated[ScoutDirectorController, Depends(get_scout_director_controller)],
) -> ScoutDirectorStatus:
    return await controller.status()
