from fastapi import APIRouter, Depends

from sherlock_homes.adapter.inbound.api.schemas.detective_watson_executor_schema import WatsonExecutorSchema, WatsonSendEmailRequest
from sherlock_homes.app.dtos.detective_watson_executor_dto import WatsonExecutorResponse, WatsonSendEmailResult
from sherlock_homes.app.ports.input.detective_watson_executor_use_case import WatsonExecutorUseCase
from sherlock_homes.dependencies.detective_watson_executor_provider import get_watson_executor_use_case

'''
존 왓슨 (John)
역할 (keyword): executor (실행/조율자)
셜록의 파트너인 사설 탐정 조력자.
탐정의 추론 결과를 실제 현실 세계의 액션과 인간의 언어(블로그 등)로 번역하고 최종 사용자 인터페이스를 조율 및 실행합니다.
'''

watson_executor_router = APIRouter(prefix="/watson", tags=["watson"])


@watson_executor_router.get("/myself")
async def introduce_myself(
    watson: WatsonExecutorUseCase = Depends(get_watson_executor_use_case)
) -> WatsonExecutorResponse:
    return await watson.introduce_myself(
        WatsonExecutorSchema(id=10, name="존 왓슨 (John)")
    )


@watson_executor_router.post("/send-email")
async def send_email(
    body: WatsonSendEmailRequest,
    watson: WatsonExecutorUseCase = Depends(get_watson_executor_use_case),
) -> WatsonSendEmailResult:
    return await watson.send_email(body)
