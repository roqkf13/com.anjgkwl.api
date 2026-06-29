from fastapi import APIRouter, Depends

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.detective_mary_operator_schema import MaryOperatorSchema
from tailor.apps.sherlock_homes.app.dtos.detective_mary_operator_dto import MaryOperatorResponse
from tailor.apps.sherlock_homes.app.ports.input.detective_mary_operator_use_case import MaryOperatorUseCase
from tailor.apps.sherlock_homes.dependencies.detective_mary_operator_provider import get_mary_operator_use_case

'''
메리 왓슨 (Mary)
역할 (keyword): operator (특수 작전/보안)
사설 탐정단에 합류한 전직 비밀 요원.
베이커가 팀의 안전을 도모하듯, 시스템 내부의 예외 처리(Exception), 보안 우회 로직 및 긴급 특수 작전 코드를 수행합니다.
'''

mary_operator_router = APIRouter(prefix="/mary", tags=["mary"])


@mary_operator_router.get("/myself")
async def introduce_myself(
    mary: MaryOperatorUseCase = Depends(get_mary_operator_use_case)
) -> MaryOperatorResponse:
    return await mary.introduce_myself(
        MaryOperatorSchema(
            id=12,
            name="메리 왓슨 (Mary)"
        )
    )
