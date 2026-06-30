from sherlock_homes.app.dtos.juso_dto import ContactCommand, ContactListResult, ContactUploadResult, JusoQuery, JusoResponse
from sherlock_homes.app.ports.output.juso_repository import JusoRepository


class JusoMemoryRepository(JusoRepository):

    async def introduce_myself(self, query: JusoQuery) -> JusoResponse:
        return JusoResponse(id=query.id, name=query.name)

    async def save_contacts(self, commands: list[ContactCommand]) -> ContactUploadResult:
        return ContactUploadResult(total=len(commands), contacts=list(commands))

    async def upsert_contacts(self, commands: list[ContactCommand]) -> ContactUploadResult:
        return ContactUploadResult(total=len(commands), contacts=list(commands))

    async def list_contacts(self) -> ContactListResult:
        return ContactListResult(total=0, contacts=[])
