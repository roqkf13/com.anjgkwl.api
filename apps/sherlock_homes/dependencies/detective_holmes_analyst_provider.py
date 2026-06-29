from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tailor.apps.sherlock_homes.adapter.outbound.pg.detective_holmes_analyst_pg_repository import HolmesAnalystPgRepository
from tailor.apps.sherlock_homes.app.ports.output.detective_holmes_analyst_repository import HolmesAnalystRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from tailor.apps.sherlock_homes.app.ports.input.detective_holmes_analyst_use_case import HolmesAnalystUseCase
from tailor.apps.sherlock_homes.app.use_cases.detective_holmes_analyst_interactor import HolmesAnalystInteractor

'''
캐릭터: 셜록 홈즈 (Sherlock)
역할 (keyword): analyst (분석가)
드라마 설정 및 시스템 기능: 경찰이 해결하지 못하는 미궁의 사건을 해결하는 사설 자문 탐정.
시스템의 가장 복잡한 추론 알고리즘을 수행하며, 핵심 데이터를 분석하여 실마리를 찾습니다.
'''

def get_holmes_analyst_use_case(
        db: AsyncSession = Depends(get_db)
) -> HolmesAnalystUseCase:
    repository: HolmesAnalystRepository = HolmesAnalystPgRepository(session=db)
    return HolmesAnalystInteractor(repository=repository)
