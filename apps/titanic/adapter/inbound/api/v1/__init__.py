from fastapi import APIRouter

from titanic.adapter.inbound.api.v1.andrews_blueprint_router import andrews_blueprint_router
from titanic.adapter.inbound.api.v1.cal_pistol_router import cal_pistol_router
from titanic.adapter.inbound.api.v1.hartley_violin_router import hartley_violin_router
from titanic.adapter.inbound.api.v1.isidor_bed_router import isidor_bed_router
from titanic.adapter.inbound.api.v1.jack_sketch_router import jack_sketch_router
from titanic.adapter.inbound.api.v1.james_director_router import james_director_router
from titanic.adapter.inbound.api.v1.rose_diamond_router import rose_diamond_router
from titanic.adapter.inbound.api.v1.ruth_corset_router import ruth_corset_router
from titanic.adapter.inbound.api.v1.smith_captain_router import smith_captain_router
from titanic.adapter.inbound.api.v1.walter_roaster_router import router as walter_router

_CHARACTER_ROUTERS = (
    andrews_blueprint_router,
    cal_pistol_router,
    hartley_violin_router,
    isidor_bed_router,
    jack_sketch_router,
    rose_diamond_router,
    ruth_corset_router,
    smith_captain_router,
    james_director_router,
    walter_router,
)

titanic_v1_router = APIRouter()
for _router in _CHARACTER_ROUTERS:
    titanic_v1_router.include_router(_router)

titanic_v1_routers = [titanic_v1_router]
