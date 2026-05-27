from fastapi import APIRouter

from titanic.adapter.inbound.api.v1.titanic_command_router import (
    router as titanic_command_router,
)
from titanic.adapter.inbound.api.v1.titanic_query_router import (
    router as titanic_query_router,
)

titanic_v1_router = APIRouter()
titanic_v1_router.include_router(titanic_command_router)
titanic_v1_router.include_router(titanic_query_router)

titanic_v1_routers = [titanic_v1_router]
