from __future__ import annotations

import asyncio
import json
import re

from sherlock_homes.app.dtos.classify_spam_dto import ClassifySpamQuery, ClassifySpamResult
from sherlock_homes.app.ports.input.classify_spam_use_case import ClassifySpamUseCase
from star_craft.domain.ontology.spam.spam_category import SpamCategory
from star_craft.domain.ontology.spam.spam_taxonomy import TAXONOMY_INDEX

_SYSTEM_PROMPT = """\
당신은 이메일 스팸 분류 전문가입니다.
주어진 이메일의 제목과 본문을 분석하여 아래 카테고리 중 하나로 분류하세요.

카테고리:
{taxonomy}

반드시 아래 JSON 형식으로만 응답하세요. 추가 설명 없이 JSON만 출력하세요.
{{"category": "<카테고리 값>", "reason": "<한 문장 이유>"}}\
"""


def _build_system_prompt() -> str:
    lines = [
        f"- {node.category.value}: {node.description}"
        for node in TAXONOMY_INDEX.values()
        if node.category is not SpamCategory.UNKNOWN
    ]
    return _SYSTEM_PROMPT.format(taxonomy="\n".join(lines))


class ClassifySpamInteractor(ClassifySpamUseCase):

    async def classify(self, query: ClassifySpamQuery) -> ClassifySpamResult:
        message = f"제목: {query.subject}\n본문: {query.body}"
        raw = await asyncio.to_thread(self._call_llm, message)
        return self._parse(raw)

    def _call_llm(self, message: str) -> str:
        from core.lol.t1_mid_faker_orchestrator import generate_reply_exaone

        return generate_reply_exaone(message=message, system=_build_system_prompt())

    def _parse(self, raw: str) -> ClassifySpamResult:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            data = json.loads(match.group())
            category = SpamCategory(data.get("category", SpamCategory.UNKNOWN))
            return ClassifySpamResult(category=category, reason=data.get("reason", ""))
        raise ValueError(f"EXAONE 응답에서 JSON을 파싱하지 못했습니다: {raw[:200]}")
