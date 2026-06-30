from __future__ import annotations

from sherlock_homes.adapter.inbound.api.schemas.juso_schema import JusoSchema
from sherlock_homes.app.dtos.juso_dto import ContactCommand, ContactListResult, ContactUploadResult, JusoQuery, JusoResponse
from sherlock_homes.app.ports.input.juso_use_case import JusoUseCase
from sherlock_homes.app.ports.output.juso_repository import JusoRepository


class JusoInteractor(JusoUseCase):

    def __init__(self, repository: JusoRepository):
        self.repository = repository

    async def introduce_myself(self, schema: JusoSchema) -> JusoResponse:
        return await self.repository.introduce_myself(JusoQuery(
            id=schema.id,
            name=schema.name,
        ))

    async def list_contacts(self) -> ContactListResult:
        return await self.repository.list_contacts()

    def _to_commands(self, rows: list) -> list[ContactCommand]:
        return [
            ContactCommand(
                first_name=r.first_name,
                middle_name=r.middle_name,
                last_name=r.last_name,
                phonetic_first_name=r.phonetic_first_name,
                phonetic_middle_name=r.phonetic_middle_name,
                phonetic_last_name=r.phonetic_last_name,
                name_prefix=r.name_prefix,
                name_suffix=r.name_suffix,
                nickname=r.nickname,
                file_as=r.file_as,
                organization_name=r.organization_name,
                organization_title=r.organization_title,
                organization_department=r.organization_department,
                birthday=r.birthday,
                notes=r.notes,
                photo=r.photo,
                labels=r.labels,
                e_mail_1_label=r.e_mail_1_label,
                e_mail_1_value=r.e_mail_1_value,
                e_mail_2_label=r.e_mail_2_label,
                e_mail_2_value=r.e_mail_2_value,
                phone_1_label=r.phone_1_label,
                phone_1_value=r.phone_1_value,
            )
            for r in rows
        ]

    async def upload_contacts(self, rows: list) -> ContactUploadResult:
        return await self.repository.save_contacts(self._to_commands(rows))

    async def upsert_contacts(self, rows: list) -> ContactUploadResult:
        return await self.repository.upsert_contacts(self._to_commands(rows))
