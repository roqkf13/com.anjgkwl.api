from typing import Annotated

from fastapi import Depends

from scout.app.repositories.game_detail_repository import GameDetailRepository
from scout.app.repositories.steam_news_repository import SteamNewsRepository
from scout.app.repositories.metroidvania_repository import MetroidvaniaRepository
from scout.app.repositories.openworld_repository import OpenworldRepository
from scout.app.repositories.roguelike_repository import RoguelikeRepository
from scout.app.repositories.soulslike_repository import SoulslikeRepository
from scout.app.services.game_detail_service import GameDetailService
from scout.app.services.patch_note_korean_service import PatchNoteKoreanService
from scout.app.services.metroidvania_service import MetroidvaniaService
from scout.app.services.openworld_service import OpenworldService
from scout.app.services.roguelike_service import RoguelikeService
from scout.app.services.soulslike_service import SoulslikeService


async def get_soulslike_repository() -> SoulslikeRepository:
    return SoulslikeRepository()


async def get_soulslike_service(
    repository: Annotated[SoulslikeRepository, Depends(get_soulslike_repository)],
) -> SoulslikeService:
    return SoulslikeService(repository)


async def get_soulslike_controller(
    service: Annotated[SoulslikeService, Depends(get_soulslike_service)],
):
    from scout.app.controllers.soulslike_controller import SoulslikeController

    return SoulslikeController(service)


async def get_roguelike_repository() -> RoguelikeRepository:
    return RoguelikeRepository()


async def get_roguelike_service(
    repository: Annotated[RoguelikeRepository, Depends(get_roguelike_repository)],
) -> RoguelikeService:
    return RoguelikeService(repository)


async def get_roguelike_controller(
    service: Annotated[RoguelikeService, Depends(get_roguelike_service)],
):
    from scout.app.controllers.roguelike_controller import RoguelikeController

    return RoguelikeController(service)


async def get_openworld_repository() -> OpenworldRepository:
    return OpenworldRepository()


async def get_openworld_service(
    repository: Annotated[OpenworldRepository, Depends(get_openworld_repository)],
) -> OpenworldService:
    return OpenworldService(repository)


async def get_openworld_controller(
    service: Annotated[OpenworldService, Depends(get_openworld_service)],
):
    from scout.app.controllers.openworld_controller import OpenworldController

    return OpenworldController(service)


async def get_metroidvania_repository() -> MetroidvaniaRepository:
    return MetroidvaniaRepository()


async def get_metroidvania_service(
    repository: Annotated[MetroidvaniaRepository, Depends(get_metroidvania_repository)],
) -> MetroidvaniaService:
    return MetroidvaniaService(repository)


async def get_metroidvania_controller(
    service: Annotated[MetroidvaniaService, Depends(get_metroidvania_service)],
):
    from scout.app.controllers.metroidvania_controller import MetroidvaniaController

    return MetroidvaniaController(service)


async def get_scout_director_controller():
    from scout.app.controllers.scout_director_controller import ScoutDirectorController

    return ScoutDirectorController()


async def get_game_detail_repository() -> GameDetailRepository:
    return GameDetailRepository()


async def get_steam_news_repository() -> SteamNewsRepository:
    return SteamNewsRepository()


async def get_patch_note_korean_service() -> PatchNoteKoreanService:
    return PatchNoteKoreanService()


async def get_game_detail_service(
    repository: Annotated[GameDetailRepository, Depends(get_game_detail_repository)],
    steam_news: Annotated[SteamNewsRepository, Depends(get_steam_news_repository)],
    patch_korean: Annotated[
        PatchNoteKoreanService, Depends(get_patch_note_korean_service)
    ],
) -> GameDetailService:
    return GameDetailService(repository, steam_news, patch_korean)


async def get_game_detail_controller(
    service: Annotated[GameDetailService, Depends(get_game_detail_service)],
):
    from scout.app.controllers.game_detail_controller import GameDetailController

    return GameDetailController(service)
