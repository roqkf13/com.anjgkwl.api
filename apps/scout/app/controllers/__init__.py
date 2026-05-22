from scout.app.controllers.game_detail_controller import router as game_detail_router
from scout.app.controllers.metroidvania_controller import router as metroidvania_router
from scout.app.controllers.openworld_controller import router as openworld_router
from scout.app.controllers.roguelike_controller import router as roguelike_router
from scout.app.controllers.scout_director_controller import router as scout_director_router
from scout.app.controllers.soulslike_controller import router as soulslike_router

__all__ = [
    "game_detail_router",
    "metroidvania_router",
    "openworld_router",
    "roguelike_router",
    "scout_director_router",
    "soulslike_router",
]

scout_routers = [
    scout_director_router,
    game_detail_router,
    soulslike_router,
    roguelike_router,
    openworld_router,
    metroidvania_router,
]
