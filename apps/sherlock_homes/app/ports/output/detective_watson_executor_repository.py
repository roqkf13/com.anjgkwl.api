from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.detective_watson_executor_dto import WatsonExecutorQuery, WatsonExecutorResponse


class WatsonExecutorRepository(ABC):

    @abstractmethod
    async def introduce_myself(self, query: WatsonExecutorQuery) -> WatsonExecutorResponse:
        pass
