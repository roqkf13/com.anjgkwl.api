from sherlock_homes.app.dtos.detective_watson_executor_dto import WatsonExecutorQuery, WatsonExecutorResponse
from sherlock_homes.app.ports.output.detective_watson_executor_repository import WatsonExecutorRepository


class WatsonMemoryRepository(WatsonExecutorRepository):

    async def introduce_myself(self, query: WatsonExecutorQuery) -> WatsonExecutorResponse:
        return WatsonExecutorResponse(id=query.id, name=query.name)
