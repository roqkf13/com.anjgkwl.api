import json
import pytest
from unittest.mock import patch

from sherlock_homes.app.use_cases.classify_spam_interactor import ClassifySpamInteractor
from sherlock_homes.app.dtos.classify_spam_dto import ClassifySpamQuery, ClassifySpamResult
from star_craft.domain.ontology.spam.spam_category import SpamCategory

LLM_PATH = "sherlock_homes.app.use_cases.classify_spam_interactor.ClassifySpamInteractor._call_llm"


@pytest.fixture
def interactor():
    return ClassifySpamInteractor()


def _llm_response(category: SpamCategory, reason: str = "테스트 이유") -> str:
    return json.dumps({"category": category.value, "reason": reason}, ensure_ascii=False)


class TestClassify:
    async def test_phishing_email(self, interactor):
        query = ClassifySpamQuery(subject="계정 확인 요청", body="비밀번호를 재설정하세요.")

        with patch(LLM_PATH, return_value=_llm_response(SpamCategory.PHISHING)):
            result = await interactor.classify(query)

        assert result.category == SpamCategory.PHISHING
        assert isinstance(result.reason, str)

    async def test_advertising_email(self, interactor):
        query = ClassifySpamQuery(subject="한정 특가 할인", body="지금 구매하세요!")

        with patch(LLM_PATH, return_value=_llm_response(SpamCategory.ADVERTISING)):
            result = await interactor.classify(query)

        assert result.category == SpamCategory.ADVERTISING

    async def test_scam_email(self, interactor):
        query = ClassifySpamQuery(subject="당신이 당첨되었습니다", body="긴급 송금이 필요합니다.")

        with patch(LLM_PATH, return_value=_llm_response(SpamCategory.SCAM)):
            result = await interactor.classify(query)

        assert result.category == SpamCategory.SCAM

    async def test_returns_reason(self, interactor):
        query = ClassifySpamQuery(subject="invoice", body="open attachment")
        expected_reason = "악성 첨부파일이 포함된 메일입니다."

        with patch(LLM_PATH, return_value=_llm_response(SpamCategory.MALWARE, expected_reason)):
            result = await interactor.classify(query)

        assert result.reason == expected_reason

    async def test_unknown_category_on_unrecognized_value(self, interactor):
        query = ClassifySpamQuery(subject="일반 메일", body="안녕하세요.")
        raw = json.dumps({"category": "unknown", "reason": "분류 불가"})

        with patch(LLM_PATH, return_value=raw):
            result = await interactor.classify(query)

        assert result.category == SpamCategory.UNKNOWN

    async def test_raises_on_invalid_json(self, interactor):
        query = ClassifySpamQuery(subject="테스트", body="본문")

        with patch(LLM_PATH, return_value="JSON이 아닌 응답"):
            with pytest.raises(ValueError, match="JSON을 파싱하지 못했습니다"):
                await interactor.classify(query)
