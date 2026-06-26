# abiswallow — 백엔드 프로젝트

Python FastAPI 기반 **모듈러 모놀리식** 서버. 일반 지침은 루트 `CLAUDE.md` 참조.

## 아키텍처 개요: 스타 토폴로지 (Star Topology)

`apps/` 안의 모듈들은 **스타 토폴로지** 구조를 따른다.

```
        friday13th
            │
scout ── star_craft ── titanic
            │
           doro
          (...)
```

- **허브(Hub)**: `apps/star_craft` — 컨텍스트 라우팅, 전역 인덱스, 앱 간 중개 담당.
- **스포크(Spoke)**: 나머지 모든 앱 모듈 — 독립적인 도메인, 허브를 통해서만 상호작용.

### 의존성 방향 규칙

| 방향 | 허용 여부 |
|------|----------|
| 스포크 → 허브 | ✅ 허용 |
| 허브 → 스포크 | ✅ 허용 |
| 스포크 → 스포크 (직접) | ❌ **금지** |
| 스포크 간 순환 참조 | ❌ **금지** |

스포크가 다른 스포크의 기능이 필요하면 반드시 허브를 경유한다.  
이 규칙은 코드 리뷰와 `import-linter`로 강제한다.

### 하네스 검증 (Harness Engineering)

구조적 제약이 깨지지 않도록 다음 도구들이 배선(harness)처럼 항상 작동한다.

| 레이어 | 도구 | 파일 |
|--------|------|------|
| Python 의존성 규칙 | `import-linter` | `setup.cfg` |
| MD 온톨로지 구조 검증 | 커스텀 스크립트 | `scripts/validate-harness.py` |
| MD 린팅 | `markdownlint` | `.markdownlint.json` |
| MD 포매팅 | `prettier` | `.prettierrc` |

- **정적 분석**: `setup.cfg`의 import-linter 규칙이 스포크 간 직접 import를 CI에서 차단.
- **온톨로지 검증**: MD 파일은 허브/스포크 노드로 취급하며, frontmatter에 `type`과 `links` 필드를 포함해야 함. `validate-harness.py`가 위반 여부를 검사.
- **테스트**: 허브의 라우팅 로직은 단위 테스트로 커버. 스포크는 허브 없이 독립 테스트 가능해야 함.
- **아키텍처 문서**: 새 앱 추가 시 허브/스포크 역할을 `apps/<name>/__init__.py` 상단 docstring에 명시.

### MD 온톨로지 노드 스키마

지식 베이스의 MD 파일은 허브 또는 스포크 노드로 선언한다.

```yaml
# 허브 노드 예시
---
type: hub
id: star_craft
title: "Star Craft Hub"
links:
  - friday13th
  - scout
  - titanic
---

# 스포크 노드 예시
---
type: spoke
id: friday13th
title: "Friday 13th — 회원/인증"
links:
  - star_craft
---
```

규칙: `links`에 다른 스포크 ID를 직접 넣으면 `validate-harness.py`가 위반으로 감지한다.

---

## 기술 스택

- **FastAPI 0.137** + **Uvicorn**
- **SQLAlchemy 2 (asyncio)** + **asyncpg** (Neon PostgreSQL)
- **Alembic** (DB 마이그레이션) + **SQLModel**
- **Google GenAI** (Gemini) + **Ollama** (로컬 LLM)
- **pytest** (`asyncio_mode = auto`)

## 디렉토리 구조

```
abiswallow/
├── main.py              ← FastAPI 앱 진입점, 라우터 등록
├── core/                ← 공유 설정, DB 엔진 (matrix/)
├── adapters/            ← 공유 어댑터 (DB 헬스 등)
├── alembic/             ← DB 마이그레이션
└── apps/                ← 도메인별 앱 모듈
    ├── star_craft/      ← [허브] 컨텍스트 라우팅, 앱 간 중개
    ├── friday13th/      ← [스포크] 회원/인증
    ├── scout/           ← [스포크] 게임 추천
    ├── titanic/         ← [스포크] Titanic 예측
    ├── doro/            ← [스포크] 데이터 분석
    └── ...
```

각 앱은 **헥사고날 아키텍처**를 따른다.

```
apps/<name>/
├── adapter/
│   ├── inbound/api/     ← FastAPI 라우터
│   └── outbound/orm/    ← SQLAlchemy 모델·리포지토리
├── app/                 ← 유스케이스
└── domain/
    ├── entities/
    └── value_objects/
```

## 개발 / 실행

```bash
# abiswallow/ 루트에서
uvicorn main:app --reload
```

## 테스트

```bash
pytest                   # 전체 (빠른 테스트)
pytest -m "not ollama"   # Ollama 없는 환경에서
pytest -m ollama         # Ollama 로컬 서버 필요
```

## 마이그레이션

```bash
alembic revision --autogenerate -m "설명"
alembic upgrade head
```

## 컨벤션

- 새 앱은 `apps/` 아래 헥사고날 구조로 추가하고 `main.py`에 라우터 등록.
- 새 앱 추가 시 허브/스포크 여부를 `apps/<name>/__init__.py` 상단 docstring에 명시.
- 스포크에서 다른 스포크를 직접 import하지 않는다. 허브(`star_craft`)를 경유한다.
- DB 모델은 `adapter/outbound/orm/`, 도메인 엔티티는 `domain/entities/`에 분리.
- 엔드포인트는 `async def` 기본. 동기 처리가 꼭 필요한 경우에만 `def`.
- 느린 LLM 테스트는 `@pytest.mark.ollama`로 마킹.
