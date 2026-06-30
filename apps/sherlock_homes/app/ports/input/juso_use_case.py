from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.adapter.inbound.api.schemas.juso_schema import JusoSchema
from sherlock_homes.app.dtos.juso_dto import ContactListResult, ContactUploadResult, JusoResponse


class JusoUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: JusoSchema) -> JusoResponse:
        pass

    @abstractmethod
    async def upload_contacts(self, rows: list) -> ContactUploadResult:
        pass

    @abstractmethod
    async def upsert_contacts(self, rows: list) -> ContactUploadResult:
        pass

    @abstractmethod
    async def list_contacts(self) -> ContactListResult:
        pass
