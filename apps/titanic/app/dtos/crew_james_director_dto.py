from __future__ import annotations

from dataclasses import dataclass

from titanic.domain.entities.crew_james_director_entity import ManifestEntry


@dataclass(frozen=True)
class ManifestRow:
    """업로드된 CSV 한 행의 원천 값(애플리케이션 입력 모델).

    어댑터(HTTP/CSV) 스키마에 유스케이스가 직접 의존하지 않도록 두는 경계 모델이다.
    값은 아직 검증되지 않은 문자열이며, 도메인 변환은 ManifestEntry.from_raw 가 담당한다.
    """
    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str
    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass(frozen=True)
class UploadManifestResult:
    """업로드 유스케이스 출력. 저장 건수와 저장된 집계를 함께 전달한다."""
    saved_count: int
    entries: list[ManifestEntry]


@dataclass(frozen=True)
class DirectorIntroduction:
    """감독 자기소개 유스케이스 출력."""
    id: int
    name: str
