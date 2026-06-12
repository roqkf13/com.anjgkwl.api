import logging
from typing import Annotated
from fastapi import APIRouter, Body, Depends

logger = logging.getLogger(__name__)
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema, SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.dependencies.crew_smith_captain_provider import get_smith_captain_use_case

'''
스미스 선장 (Captain Edward John Smith)
타이타닉의 총책임자. 침몰하는 배와 운명을 함께한 명장.
전체 승객 현황(생존/사망 통계)을 관장하는 마스터 역할.

추천 파일명: smith_captain_router.py (또는 smith_wheel_router.py)
'''

smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])


@smith_captain_router.post("/chat")
async def chat(
    schema: Annotated[ChatSchema, Body()],
) -> dict:
    # abiswallow 에서 smith/page.tsx 에서 /titanic/smith/chat
    # 이 URL로 키값이 messages 인 Body() 로
    #  보낸 내용을 로그로 출력하는 코드
    for msg in schema.messages:
        logger.info(f"[smith/chat] role={msg.role} text={msg.text}")
    return {"text": schema.messages[-1].text if schema.messages else ""}

@smith_captain_router.get("/myself")
async def introduce_myself(
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case)
) -> SmithCaptainResponse :
    return await smith.introduce_myself(
        SmithCaptainSchema(
            id=7,
            name="스미스 선장 (Captain Edward John Smith)"
        )
    )