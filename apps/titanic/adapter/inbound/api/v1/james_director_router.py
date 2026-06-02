from __future__ import annotations

import csv
from io import StringIO
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from titanic.adapter.inbound.api.deps import get_james_director_use_case
from titanic.adapter.inbound.api.schemas.james_director_schema import (
    JamesDirectorListResponse,
    JamesDirectorUploadResponse,
)
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase


james_director_router = APIRouter(prefix="/titanic/james_director", tags=["james_director"])

_HEADER_ALIASES: dict[str, str] = {
    "passengerid": "passenger_id",
    "passenger_id": "passenger_id",
    "passenger": "passenger_id",
    "survived": "survived",
    "pclass": "pclass",
    "name": "name",
    "sex": "gender",
    "gender": "gender",
    "age": "age",
    "sibsp": "sib_sp",
    "sib_sp": "sib_sp",
    "parch": "parch",
    "ticket": "ticket",
    "fare": "fare",
    "cabin": "cabin",
    "embarked": "embarked",
}


def _normalize_titanic_row(row: dict[str, Any]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        alias = _HEADER_ALIASES.get(raw_key.strip().lower())
        if alias is None:
            continue
        normalized[alias] = "" if value is None else str(value).strip()
    return normalized


async def _parse_csv_file(file: UploadFile) -> list[dict[str, str]]:
    filename = (file.filename or "").lower()
    if not filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")

    text = raw.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")

    return [_normalize_titanic_row(row) for row in reader]


@james_director_router.get("/passengers", response_model=JamesDirectorListResponse)
async def list_passengers(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    use_case: JamesDirectorUseCase = Depends(get_james_director_use_case),
) -> JamesDirectorListResponse:
    result = await use_case.list_passengers(page, page_size)
    return JamesDirectorListResponse(**result)


@james_director_router.post("/upload", response_model=JamesDirectorUploadResponse)
async def upload_titanic_file(
    file: UploadFile = File(...),
    use_case: JamesDirectorUseCase = Depends(get_james_director_use_case),
) -> JamesDirectorUploadResponse:
    """Titanic CSV 파일을 업로드하고 NeonDB에 저장합니다."""
    normalized_rows = await _parse_csv_file(file)
    if not normalized_rows:
        raise HTTPException(status_code=400, detail="저장할 행이 없습니다.")

    result = await use_case.receive_uploaded_records(normalized_rows)
    return JamesDirectorUploadResponse(**result)
