from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from scout.app.deps import get_game_detail_controller
from scout.app.schemas.game_detail_schema import GameDetailSchema, PatchNoteSchema
from scout.app.services.game_detail_service import GameDetailService

router = APIRouter(prefix="/scout/games", tags=["scout"])


class GameDetailController:
    def __init__(self, service: GameDetailService) -> None:
        self._service = service

    async def get_detail(self, steam_app_id: int) -> GameDetailSchema:
        detail = await self._service.get_game_detail(steam_app_id)
        if not detail:
            raise HTTPException(status_code=404, detail="게임을 찾을 수 없습니다.")
        return detail

    async def translate_patch_note(
        self, steam_app_id: int, note_id: str
    ) -> PatchNoteSchema:
        note = await self._service.translate_patch_note(steam_app_id, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="패치 노트를 찾을 수 없습니다.")
        return note


@router.get(
    "/{steam_app_id}/detail",
    response_model=GameDetailSchema,
    response_model_by_alias=True,
)
async def get_scout_game_detail(
    steam_app_id: int,
    controller: Annotated[GameDetailController, Depends(get_game_detail_controller)],
) -> GameDetailSchema:
    return await controller.get_detail(steam_app_id)


@router.get(
    "/{steam_app_id}/patch-notes/{note_id}/korean",
    response_model=PatchNoteSchema,
    response_model_by_alias=True,
)
async def get_scout_patch_note_korean(
    steam_app_id: int,
    note_id: str,
    controller: Annotated[GameDetailController, Depends(get_game_detail_controller)],
) -> PatchNoteSchema:
    return await controller.translate_patch_note(steam_app_id, note_id)
