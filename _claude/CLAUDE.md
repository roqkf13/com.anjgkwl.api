# Backend (abiswallow) 지침

## 프로젝트 개요

Karpathy의 Harness Engineering 프로세스를 적용한 PKS(Personal Knowledge System). Wiki + LLM을 결합한다.

- **런타임**: Python 3.13, FastAPI, SQLAlchemy async, Uvicorn
- **DB**: PostgreSQL (Neon serverless), SQLModel/SQLAlchemy ORM
- **인프라**: Docker Compose (`./abiswallow:/app` 볼륨 마운트)
- **앱 구조**: `apps/` 하위에 독립 앱들이 시블링으로 확장된다 (titanic, friday13th, scout, …)

---

## 아키텍처 원칙

모든 코드는 예외 없이 아래를 준수한다.

- **SOLID** — Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Hexagonal Architecture** (Ports & Adapters) — 도메인 로직은 인프라에 의존하지 않는다
- **Clean Architecture** — 의존성 화살표는 항상 안쪽을 향한다 (domain ← application ← adapter)
- **DDD** — 엔티티, 값 객체, 애그리거트, 레포지토리, 유스케이스를 명시적으로 모델링한다

---

## 모듈 경로 규칙

### 앱 내부 import
`abiswallow`와 `apps` 경로 세그먼트를 생략한다.

```python
# 올바름
from titanic.adapter.inbound...
from titanic.app.ports...

# 틀림
from abiswallow.apps.titanic.adapter...
```

### core 모듈 import
`core.matrix.*` 경로를 직접 사용한다. re-export shim은 만들지 않는다.

```python
# 올바름
from core.matrix.grid_oracle_database_manager import get_db
from core.matrix.vault_keymaker_secret_manager import generate_reply

# 틀림
from core.database import get_db
from abiswallow.core.database import get_db
```

### sys.path 구조
`main.py`가 `/app`(abiswallow 루트)과 `/app/apps`를 `sys.path`에 추가한다.  
따라서 `titanic.*`, `friday13th.*`, `core.*` 모두 최상위에서 직접 import된다.

---

## core/matrix 공유 인프라

| 파일 | 역할 |
|------|------|
| `grid_oracle_database_manager.py` | AsyncSession 팩토리, 테이블 생성, `get_db` |
| `vault_keymaker_secret_manager.py` | Gemini API 클라이언트 (`generate_reply` 등) |
| `gird_neo_theone_base.py` | SQLAlchemy `DeclarativeBase` |
| `chat_router.py` | `/chat` 엔드포인트 (Gemini 연동) |

`core/matrix/__init__.py`는 비워 둔다. 각 모듈을 직접 import한다.

---

## 앱별 세부 지침

@./apps/titanic/_docs/CLAUDE.md
