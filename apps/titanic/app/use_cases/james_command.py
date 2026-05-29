from __future__ import annotations

from typing import Any

from titanic.app.ports.output.james_repository import JamesRepository

_ALLOWED_KEYS = frozenset({
    "passenger",
    "survived",
    "pclass",
    "name",
    "gender",
    "age",
    "sibsp",
    "parch",
    "ticket",
    "fare",
    "cabin",
    "embarked",
})


def _prepare_records(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    prepared: list[dict[str, str]] = []
    for row in records:
        item: dict[str, str] = {}
        for key, value in row.items():
            if key not in _ALLOWED_KEYS:
                continue
            item[key] = "" if value is None else str(value).strip()
        prepared.append(item)
    return prepared


class JamesCommand:
    """업로드 레코드를 출력 포트(JamesRepository)에 저장합니다."""

    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def receive_uploaded_records(
        self, records: list[dict[str, Any]]
    ) -> dict[str, Any]:
        prepared = _prepare_records(records)
        saved = await self._repository.save_all(prepared)
        return {
            "count": len(prepared),
            "records": prepared,
            "stored_count": saved,
            "message": f"{saved}건을 Neon에 저장했습니다.",
        }
