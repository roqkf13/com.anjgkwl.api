"""Steam 패치 노트 영문을 Gemini API로 한국어 번역."""

from __future__ import annotations

import asyncio
import json
import logging
import re
import time

from scout.app.repositories.patch_translation_store import (
    is_korean_translation,
    load as load_persisted,
    save as save_persisted,
)
from scout.app.schemas.game_detail_schema import PatchNoteSchema

logger = logging.getLogger(__name__)

_TRANSLATE_MAX_CHARS = 12_000
_MAX_ATTEMPTS = 4
_MIN_INTERVAL_SEC = 5.0
_FAIL_PREFIX = "【번역 안내】자동 번역에 실패해 Steam 원문(영어)입니다.\n\n"

_translation_cache: dict[str, PatchNoteSchema] = {}
_last_call_at: float = 0.0


def _wait_rate_limit() -> None:
    global _last_call_at
    elapsed = time.monotonic() - _last_call_at
    if elapsed < _MIN_INTERVAL_SEC:
        time.sleep(_MIN_INTERVAL_SEC - elapsed)
    _last_call_at = time.monotonic()


def _parse_json_response(raw: str) -> dict:
    text = raw.strip()
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.I)
    if fenced:
        text = fenced.group(1).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("JSON not found")
    return json.loads(text[start : end + 1])


def _is_rate_limit(err: Exception) -> bool:
    m = str(err).lower()
    return "429" in m or "quota" in m


def _retry_delay(err: Exception) -> float:
    m = re.search(r"retry in ([\d.]+)s", str(err), re.I)
    return float(m.group(1)) + 2.0 if m else _MIN_INTERVAL_SEC


class PatchNoteKoreanService:
    async def translate(self, note: PatchNoteSchema, *, body_en: str) -> PatchNoteSchema:
        persisted = load_persisted(note.id)
        if persisted:
            _translation_cache[note.id] = persisted
            return persisted

        cached = _translation_cache.get(note.id)
        if cached and is_korean_translation(cached):
            return cached

        from matrix.app.keymaker import is_gemini_configured

        if not is_gemini_configured():
            return note.model_copy(
                update={
                    "body_ko": "【번역 안내】GEMINI_API_KEY가 없어 원문(영어)입니다.\n\n"
                    + body_en,
                    "summary": "Steam 원문(영어). API 키 설정 시 한글 번역됩니다.",
                }
            )

        try:
            translated = await asyncio.to_thread(
                self._translate_with_retry, note, body_en
            )
            _translation_cache[note.id] = translated
            if is_korean_translation(translated):
                save_persisted(translated)
            return translated
        except Exception as e:
            logger.warning(
                "[PatchNoteKoreanService] failed id=%s err=%s", note.id, e
            )
            return note.model_copy(
                update={
                    "body_ko": _FAIL_PREFIX + body_en,
                    "summary": note.summary[:200],
                }
            )

    def _translate_with_retry(
        self, note: PatchNoteSchema, body_en: str
    ) -> PatchNoteSchema:
        last: Exception | None = None
        for attempt in range(_MAX_ATTEMPTS):
            try:
                return self._translate_one(note, body_en)
            except Exception as e:
                last = e
                if attempt >= _MAX_ATTEMPTS - 1 or not _is_rate_limit(e):
                    raise
                time.sleep(_retry_delay(e))
        raise last or RuntimeError("translate failed")

    def _translate_one(self, note: PatchNoteSchema, body_en: str) -> PatchNoteSchema:
        from matrix.app.keymaker import generate_reply

        text = body_en[:_TRANSLATE_MAX_CHARS]
        prompt = (
            "Steam 게임 패치 노트를 한국어로 번역하세요. 자연스럽고 읽기 쉽게.\n"
            "카드·유물·스킬 이름은 정확히. 섹션은 '콘텐츠 & 밸런스' 형식, 항목은 '- ' 불릿.\n"
            "JSON만 출력: "
            '{"title_ko":"","summary_ko":"220자 이내","body_ko":"전체 본문"}\n'
            "body_ko 줄바꿈은 \\n\n\n"
            f"제목: {note.title}\n\n본문:\n{text}\n\n번역해줘."
        )
        _wait_rate_limit()
        raw = generate_reply(message=prompt)
        data = _parse_json_response(raw)
        body_ko = (data.get("body_ko") or "").strip()
        if not body_ko:
            raise ValueError("empty body_ko")
        return note.model_copy(
            update={
                "title": (data.get("title_ko") or note.title).strip(),
                "summary": (data.get("summary_ko") or note.summary).strip()[:220],
                "body_ko": body_ko,
            }
        )
