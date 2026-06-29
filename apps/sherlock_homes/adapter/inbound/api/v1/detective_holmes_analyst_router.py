from fastapi import APIRouter, Depends

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.detective_holmes_analyst_schema import HolmesAnalystSchema
from tailor.apps.sherlock_homes.app.dtos.detective_holmes_analyst_dto import HolmesAnalystResponse
from tailor.apps.sherlock_homes.app.ports.input.detective_holmes_analyst_use_case import HolmesAnalystUseCase
from tailor.apps.sherlock_homes.dependencies.detective_holmes_analyst_provider import get_holmes_analyst_use_case

'''
셜록 홈즈 (Sherlock)
역할 (keyword): analyst (분석가)
경찰이 해결하지 못하는 미궁의 사건을 해결하는 사설 자문 탐정.
시스템의 가장 복잡한 추론 알고리즘을 수행하며, 핵심 데이터를 분석하여 실마리를 찾습니다.
'''

holmes_analyst_router = APIRouter(prefix="/holmes", tags=["holmes"])


@holmes_analyst_router.get("/myself")
async def introduce_myself(
    holmes: HolmesAnalystUseCase = Depends(get_holmes_analyst_use_case)
) -> HolmesAnalystResponse:
    return await holmes.introduce_myself(
        HolmesAnalystSchema(
            id=9,
            name="셜록 홈즈 (Sherlock)"
        )
    )
