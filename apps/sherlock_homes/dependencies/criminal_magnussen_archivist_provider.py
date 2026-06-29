from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tailor.apps.sherlock_homes.adapter.outbound.pg.criminal_magnussen_archivist_pg_repository import MagnussenArchivistPgRepository
from tailor.apps.sherlock_homes.app.ports.output.criminal_magnussen_archivist_repository import MagnussenArchivistRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from tailor.apps.sherlock_homes.app.ports.input.criminal_magnussen_archivist_use_case import MagnussenArchivistUseCase
from tailor.apps.sherlock_homes.app.use_cases.criminal_magnussen_archivist_interactor import MagnussenArchivistInteractor

'''
캐릭터: 마그누센 (Magnussen)
역할 (keyword): archivist (전략 데이터 아카이브)
드라마 설정 및 시스템 기능: 모든 유력 인사의 약점을 뇌 속 마인드 팰리스에 담아두고 협박하는 미디어 거물.
전략적 대립에 필요한 거대 규모의 장기 아카이브 데이터를 구조화하고 보관합니다.
'''

def get_magnussen_archivist_use_case(
        db: AsyncSession = Depends(get_db)
) -> MagnussenArchivistUseCase:
    repository: MagnussenArchivistRepository = MagnussenArchivistPgRepository(session=db)
    return MagnussenArchivistInteractor(repository=repository)
