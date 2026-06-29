from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tailor.apps.sherlock_homes.adapter.outbound.pg.police_anderson_collector_pg_repository import AndersonCollectorPgRepository
from tailor.apps.sherlock_homes.app.ports.output.police_anderson_collector_repository import AndersonCollectorRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from tailor.apps.sherlock_homes.app.ports.input.police_anderson_collector_use_case import AndersonCollectorUseCase
from tailor.apps.sherlock_homes.app.use_cases.police_anderson_collector_interactor import AndersonCollectorInteractor

'''
캐릭터: 앤더슨 (Anderson)
역할 (keyword): collector (로그/수집가)
드라마 설정 및 시스템 기능: 런던 경시청의 감식반원(이후 셜록의 팬클럽 결성).
현장의 원시 데이터를 수집하고 시스템의 초기 로그 및 로우(Raw) 데이터를 정제합니다.
'''

def get_anderson_collector_use_case(
        db: AsyncSession = Depends(get_db)
) -> AndersonCollectorUseCase:
    repository: AndersonCollectorRepository = AndersonCollectorPgRepository(session=db)
    return AndersonCollectorInteractor(repository=repository)
