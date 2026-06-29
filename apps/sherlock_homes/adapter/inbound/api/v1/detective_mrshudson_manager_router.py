from fastapi import APIRouter, Depends

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.detective_mrshudson_manager_schema import MrshudsonManagerSchema
from tailor.apps.sherlock_homes.app.dtos.detective_mrshudson_manager_dto import MrshudsonManagerResponse
from tailor.apps.sherlock_homes.app.ports.input.detective_mrshudson_manager_use_case import MrshudsonManagerUseCase
from tailor.apps.sherlock_homes.dependencies.detective_mrshudson_manager_provider import get_mrshudson_manager_use_case

'''
허드슨 부인 (Mrs. Hudson)
역할 (keyword): manager (세션/환경 관리)
사설 탐정들의 아지트인 베이커가 221B의 집주인.
셜록과 존이 자유롭게 활동할 수 있도록 에이전트의 세션 상태와 런타임 인프라 환경을 안정적으로 관리합니다.
'''

mrshudson_manager_router = APIRouter(prefix="/mrshudson", tags=["mrshudson"])


@mrshudson_manager_router.get("/myself")
async def introduce_myself(
    mrshudson: MrshudsonManagerUseCase = Depends(get_mrshudson_manager_use_case)
) -> MrshudsonManagerResponse:
    return await mrshudson.introduce_myself(
        MrshudsonManagerSchema(
            id=11,
            name="허드슨 부인 (Mrs. Hudson)"
        )
    )
