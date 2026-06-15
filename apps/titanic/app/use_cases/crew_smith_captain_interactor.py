from __future__ import annotations

import logging

from fastapi import Depends

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatResponse, ChatSchema, SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor
from titanic.app.use_cases.passenger_rose_model_interactor import RoseModelInteractor
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case
from titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case

logger = logging.getLogger(__name__)

class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository: SmithCaptainRepository):
        self.repository = repository
  

    async def chat(self, schema: ChatSchema,
                   jack: JackTrainerUseCase = Depends(get_jack_trainer_use_case),
                   rose: RoseModelUseCase = Depends(get_rose_model_use_case)
                   ) -> ChatResponse:
        logger.info(f"[SmithCaptainInteractor] chat 진입 | messages={schema.messages}")

        return ChatResponse(text="1309명 입니다")


    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(SmithCaptainQuery(
            id = schema.id,
            name = schema.name
        ))

 