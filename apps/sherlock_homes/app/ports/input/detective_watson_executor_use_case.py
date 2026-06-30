from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.adapter.inbound.api.schemas.detective_watson_executor_schema import (
    WatsonExecutorSchema,
    WatsonSendEmailRequest,
)
from sherlock_homes.app.dtos.detective_watson_executor_dto import WatsonExecutorResponse, WatsonSendEmailResult


class WatsonExecutorUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: WatsonExecutorSchema) -> WatsonExecutorResponse:
        pass

    @abstractmethod
    async def send_email(self, schema: WatsonSendEmailRequest) -> WatsonSendEmailResult:
        pass
