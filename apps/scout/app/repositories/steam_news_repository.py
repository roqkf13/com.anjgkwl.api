"""Steam ISteamNews API에서 패치 노트 원문을 가져온다."""

from __future__ import annotations

import asyncio
import html
import json
import logging
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from scout.app.schemas.game_detail_schema import PatchNoteSchema

logger = logging.getLogger(__name__)

_STEAM_NEWS_URL = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
_DEFAULT_COUNT = 5
_FETCH_TIMEOUT_SEC = 20


def bbcode_to_plain_text(raw: str) -> str:
    if not raw:
        return ""
    s = html.unescape(raw)
    s = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", s, flags=re.I)
    s = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", s, flags=re.I)
    s = re.sub(r"<img[^>]*>", "", s, flags=re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</p>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\[img\][^\[]*\[/img\]", "", s, flags=re.I | re.DOTALL)
    s = re.sub(r"\{STEAM_CLAN_IMAGE\}[^\]]*", "", s)
    for tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
        s = re.sub(rf"\[/?{tag}\]", "\n", s, flags=re.I)
    s = re.sub(r"\[/?b\]", "", s, flags=re.I)
    s = re.sub(r"\[/?i\]", "", s, flags=re.I)
    s = re.sub(r"\[/?u\]", "", s, flags=re.I)
    s = re.sub(r"\[/?list\]", "\n", s, flags=re.I)
    s = re.sub(r"\[\*\]", "· ", s)
    s = re.sub(r"\[url=([^\]]+)\]([^\[]*)\[/url\]", r"\2", s, flags=re.I)
    s = re.sub(r"\[url\]([^\[]*)\[/url\]", r"\1", s, flags=re.I)
    s = re.sub(r"\[/?quote\]", "\n", s, flags=re.I)
    s = re.sub(r"\[/?code\]", "", s, flags=re.I)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


class SteamNewsRepository:
    async def fetch_patch_notes(
        self, steam_app_id: int, *, count: int = _DEFAULT_COUNT
    ) -> list[PatchNoteSchema]:
        return await asyncio.to_thread(self._fetch_sync, steam_app_id, count)

    def _fetch_sync(self, steam_app_id: int, count: int) -> list[PatchNoteSchema]:
        params = urllib.parse.urlencode(
            {"appid": steam_app_id, "count": count, "maxlength": 0}
        )
        url = f"{_STEAM_NEWS_URL}?{params}"
        try:
            with urllib.request.urlopen(url, timeout=_FETCH_TIMEOUT_SEC) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            logger.warning(
                "[SteamNewsRepository] fetch failed steam_app_id=%s err=%s",
                steam_app_id,
                e,
            )
            return []

        items = (payload.get("appnews") or {}).get("newsitems") or []
        notes: list[PatchNoteSchema] = []
        for item in items:
            url = (item.get("url") or "").lower()
            # 공식 패치 노트(Steam 커뮤니티 공지)만 — PCGamesN 등 외부 기사 제외
            if "steam_community_announcement" not in url:
                continue
            gid = str(item.get("gid") or "").strip()
            title = (item.get("title") or "").strip()
            body = bbcode_to_plain_text((item.get("contents") or "").strip())
            if not gid or not title or not body:
                continue
            published = datetime.fromtimestamp(
                int(item.get("date") or 0), tz=timezone.utc
            ).strftime("%Y-%m-%d")
            source = (item.get("url") or "").strip() or None
            notes.append(
                PatchNoteSchema(
                    id=f"{steam_app_id}-steam-{gid}",
                    title=title,
                    published_at=published,
                    summary=body[:220] + ("…" if len(body) > 220 else ""),
                    body_ko=body,
                    source_url=source,
                )
            )
        return notes
