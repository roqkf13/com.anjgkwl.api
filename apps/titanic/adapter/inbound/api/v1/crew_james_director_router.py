from io import StringIO
import csv

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import (
    IntroduceResponseSchema,
    ManifestRecordSchema,
    UploadResponseSchema,
)
from titanic.app.dtos.crew_james_director_dto import ManifestRow, UploadManifestResult
from titanic.app.ports.input.crew_james_director_use_case import (
    IntroduceDirectorUseCase,
    UploadTitanicManifestUseCase,
)
from titanic.dependencies.crew_james_director_provider import (
    get_introduce_director_use_case,
    get_upload_manifest_use_case,
)

'''
 james_director_router.py
 전설적인 흥행작 <타이타닉>을 연출하여
 "내가 세상의 왕이다!"를 외친 제임스 카메론 감독의 라우터
 완벽주의 성향으로 타이타닉의 모든 세트와 디테일을
 고증한 아키텍처의 총괄 디렉터 역할 수행
'''
james_director_router = APIRouter(prefix="/james", tags=["james"])


@james_director_router.get("/myself", response_model=IntroduceResponseSchema)
async def introduce_myself(
    use_case: IntroduceDirectorUseCase = Depends(get_introduce_director_use_case),
):
    intro = await use_case.introduce(director_id=6, name="제임스 카메론 (James Carmeron)")
    return IntroduceResponseSchema(id=intro.id, name=intro.name)


@james_director_router.post(
    "/upload",
    response_model=UploadResponseSchema,
    summary="타이타닉 승객 명단 CSV 파일 업로드",
)
async def upload_titanic_file(
    file: UploadFile = File(...),
    use_case: UploadTitanicManifestUseCase = Depends(get_upload_manifest_use_case),
):
    rows = _parse_csv((await file.read()).decode("utf-8", errors="replace"))
    try:
        result = await use_case.upload(rows)
    except ValueError as exc:  # 도메인 불변식 위반 → 잘못된 입력
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _to_response(result)


def _parse_csv(text: str) -> list[ManifestRow]:
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")
    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")
    return [_to_manifest_row(row) for row in reader]


def _to_manifest_row(row: dict) -> ManifestRow:
    cells = {
        key.strip().lower(): (value or "")
        for key, value in row.items()
        if key is not None
    }
    return ManifestRow(
        passenger_id=cells.get("passengerid", ""),
        name=cells.get("name", ""),
        gender=cells.get("sex", ""),  # CSV 의 Sex → 도메인 gender
        age=cells.get("age", ""),
        sib_sp=cells.get("sibsp", ""),
        parch=cells.get("parch", ""),
        survived=cells.get("survived", ""),
        pclass=cells.get("pclass", ""),
        ticket=cells.get("ticket", ""),
        fare=cells.get("fare", ""),
        cabin=cells.get("cabin", ""),
        embarked=cells.get("embarked", ""),
    )


def _to_response(result: UploadManifestResult) -> UploadResponseSchema:
    records = [
        ManifestRecordSchema(
            passenger_id=entry.id.value,
            name=entry.name.value,
            gender=entry.gender.value,
            age=_age_to_str(entry),
            sib_sp=str(entry.family.siblings_spouses),
            parch=str(entry.family.parents_children),
            survived=str(entry.survival.value) if entry.survival is not None else None,
        )
        for entry in result.entries
    ]
    return UploadResponseSchema(count=result.saved_count, records=records)


def _age_to_str(entry) -> str | None:
    if entry.age is None:
        return None
    value = entry.age.value
    return str(int(value)) if value.is_integer() else str(value)
