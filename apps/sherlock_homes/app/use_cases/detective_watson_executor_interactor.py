from __future__ import annotations

import asyncio
import json
import re

from sherlock_homes.adapter.inbound.api.schemas.detective_watson_executor_schema import WatsonExecutorSchema, WatsonSendEmailRequest
from sherlock_homes.app.dtos.detective_watson_executor_dto import (
    WatsonExecutorQuery,
    WatsonExecutorResponse,
    WatsonSendEmailQuery,
    WatsonSendEmailResult,
)
from sherlock_homes.app.ports.input.detective_watson_executor_use_case import WatsonExecutorUseCase
from sherlock_homes.app.ports.output.detective_watson_executor_repository import WatsonExecutorRepository
from sherlock_homes.app.ports.output.watson_email_gateway_port import WatsonEmailGatewayPort

_SYSTEM_PROMPT = """\
당신은 전문 이메일 작성 도우미입니다. 사용자의 요청을 바탕으로 정중하고 명확한 한국어 이메일을 작성합니다.
반드시 아래 JSON 형식으로만 응답하세요. 추가 설명 없이 JSON만 출력하세요.
{"subject": "이메일 제목", "body": "이메일 본문 내용"}\
"""


class WatsonExecutorInteractor(WatsonExecutorUseCase):

    def __init__(self, repository: WatsonExecutorRepository, email_gateway: WatsonEmailGatewayPort):
        self.repository = repository
        self.email_gateway = email_gateway

    async def introduce_myself(self, schema: WatsonExecutorSchema) -> WatsonExecutorResponse:
        return await self.repository.introduce_myself(WatsonExecutorQuery(
            id=schema.id,
            name=schema.name,
        ))

    async def send_email(self, schema: WatsonSendEmailRequest) -> WatsonSendEmailResult:
        subject, body = await asyncio.to_thread(self._generate_email_content, schema.prompt)
        query = WatsonSendEmailQuery(
            to=str(schema.to),
            prompt=schema.prompt,
            from_account=str(schema.from_account),
        )
        return await self.email_gateway.send_email(query, subject=subject, body=body)

    def _generate_email_content(self, prompt: str) -> tuple[str, str]:
        from core.lol.t1_mid_faker_orchestrator import generate_reply_exaone

        raw = generate_reply_exaone(message=prompt, system=_SYSTEM_PROMPT)
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return data.get("subject", ""), data.get("body", "")
        raise ValueError(f"EXAONE 응답에서 JSON을 파싱하지 못했습니다: {raw[:200]}")
