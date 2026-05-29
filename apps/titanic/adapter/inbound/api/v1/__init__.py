from fastapi import APIRouter

from titanic.adapter.inbound.api.v1.james_router import james_router
from titanic.adapter.inbound.api.v1.walter_router import router as walter_router

titanic_v1_router = APIRouter()
titanic_v1_router.include_router(james_router)
titanic_v1_router.include_router(walter_router)

titanic_v1_routers = [titanic_v1_router]
