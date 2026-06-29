from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tailor.apps.sherlock_homes.adapter.outbound.pg.police_molly_examiner_pg_repository import MollyExaminerPgRepository
from tailor.apps.sherlock_homes.app.ports.output.police_molly_examiner_repository import MollyExaminerRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from tailor.apps.sherlock_homes.app.ports.input.police_molly_examiner_use_case import MollyExaminerUseCase
from tailor.apps.sherlock_homes.app.use_cases.police_molly_examiner_interactor import MollyExaminerInteractor

'''
캐릭터: 몰리 후퍼 (Molly)
역할 (keyword): examiner (검증/조사관)
드라마 설정 및 시스템 기능: 세인트 바톨로뮤 병원의 부검의.
공식적인 과학 수사 데이터와 증거를 제공하듯, 시스템에 유입되는 데이터의 유효성 검증(Validation) 및 팩트 체크를 수행합니다.
'''

def get_molly_examiner_use_case(
        db: AsyncSession = Depends(get_db)
) -> MollyExaminerUseCase:
    repository: MollyExaminerRepository = MollyExaminerPgRepository(session=db)
    return MollyExaminerInteractor(repository=repository)
