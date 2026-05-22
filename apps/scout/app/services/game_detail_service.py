import logging

from scout.app.repositories.game_detail_repository import GameDetailRepository
from scout.app.repositories.patch_translation_store import (
    is_korean_translation,
    load as load_persisted,
)
from scout.app.repositories.steam_news_repository import SteamNewsRepository
from scout.app.schemas.game_detail_schema import GameDetailSchema, PatchNoteSchema
from scout.app.services.patch_note_korean_service import PatchNoteKoreanService

logger = logging.getLogger(__name__)

# steam_app_id -> note_id -> 영문 본문 (클릭 시 번역용)
_steam_body_en: dict[int, dict[str, str]] = {}


class GameDetailService:
    def __init__(
        self,
        repository: GameDetailRepository,
        steam_news: SteamNewsRepository,
        patch_korean: PatchNoteKoreanService,
    ) -> None:
        self._repository = repository
        self._steam_news = steam_news
        self._patch_korean = patch_korean

    async def get_game_detail(self, steam_app_id: int) -> GameDetailSchema | None:
        detail = await self._repository.get_detail(steam_app_id)
        if not detail:
            return None

        steam_notes = await self._steam_news.fetch_patch_notes(steam_app_id)
        if steam_notes:
            raw_map: dict[str, str] = {}
            list_notes: list[PatchNoteSchema] = []
            from_cache = 0
            for note in steam_notes:
                body_en = note.body_ko
                raw_map[note.id] = body_en
                persisted = load_persisted(note.id)
                if persisted and is_korean_translation(persisted):
                    list_notes.append(
                        persisted.model_copy(update={"body_ko": ""})
                    )
                    from_cache += 1
                    continue

                excerpt = (body_en or note.summary or "")[:220].strip()
                list_notes.append(
                    note.model_copy(
                        update={
                            "body_ko": "",
                            "summary": excerpt or note.summary,
                        }
                    )
                )

            _steam_body_en[steam_app_id] = raw_map
            detail = detail.model_copy(update={"patch_notes": list_notes})
            logger.info(
                "[GameDetailService] steam notes list steam_app_id=%s "
                "count=%s summary_from_cache=%s (body on /korean)",
                steam_app_id,
                len(list_notes),
                from_cache,
            )
        else:
            from scout.app.repositories.game_detail_repository import (
                _PATCH_NOTES_KO,
                _default_patch_notes_ko,
            )

            fallback = _PATCH_NOTES_KO.get(steam_app_id) or _default_patch_notes_ko(
                steam_app_id
            )
            detail = detail.model_copy(update={"patch_notes": fallback})
            logger.info(
                "[GameDetailService] static fallback steam_app_id=%s count=%s",
                steam_app_id,
                len(fallback),
            )

        return detail

    async def translate_patch_note(
        self, steam_app_id: int, note_id: str
    ) -> PatchNoteSchema | None:
        persisted = load_persisted(note_id)
        if persisted:
            return persisted

        body_en = (_steam_body_en.get(steam_app_id) or {}).get(note_id)

        steam_notes = await self._steam_news.fetch_patch_notes(steam_app_id)
        base = next((n for n in steam_notes if n.id == note_id), None)

        if base and not body_en:
            body_en = base.body_ko
            _steam_body_en.setdefault(steam_app_id, {})[note_id] = body_en

        if base and body_en:
            translated = await self._patch_korean.translate(base, body_en=body_en)
            if not translated.body_ko.startswith("【번역 안내】"):
                return translated
            fallback = await self._static_fallback(steam_app_id, base)
            if fallback:
                return fallback
            return translated

        detail = await self._repository.get_detail(steam_app_id)
        if not detail:
            return None
        static_note = next((n for n in detail.patch_notes if n.id == note_id), None)
        if static_note and static_note.body_ko:
            return static_note
        return None

    async def _static_fallback(
        self, steam_app_id: int, steam_note: PatchNoteSchema
    ) -> PatchNoteSchema | None:
        detail = await self._repository.get_detail(steam_app_id)
        if not detail or not detail.patch_notes:
            return None
        static = detail.patch_notes[0]
        if not static.body_ko or static.body_ko.startswith("【"):
            return None
        return static.model_copy(
            update={
                "id": steam_note.id,
                "title": steam_note.title,
                "published_at": steam_note.published_at,
                "source_url": steam_note.source_url or static.source_url,
                "summary": static.summary,
            }
        )
