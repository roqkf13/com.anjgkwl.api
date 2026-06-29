from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tailor.apps.sherlock_homes.adapter.outbound.pg.detective_mrshudson_manager_pg_repository import MrshudsonManagerPgRepository
from tailor.apps.sherlock_homes.app.ports.output.detective_mrshudson_manager_repository import MrshudsonManagerRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from tailor.apps.sherlock_homes.app.ports.input.detective_mrshudson_manager_use_case import MrshudsonManagerUseCase
from tailor.apps.sherlock_homes.app.use_cases.detective_mrshudson_manager_interactor import MrshudsonManagerInteractor

'''
캐릭터: 허드슨 부인 (Mrs. Hudson)
역할 (keyword): manager (세션/환경 관리)
드라마 설정 및 시스템 기능: 사설 탐정들의 아지트인 베이커가 221B의 집주인.
셜록과 존이 자유롭게 활동할 수 있도록 에이전트의 세션 상태와 런타임 인프라 환경을 안정적으로 관리합니다.
'''

def get_mrshudson_manager_use_case(
        db: AsyncSession = Depends(get_db)
) -> MrshudsonManagerUseCase:
    repository: MrshudsonManagerRepository = MrshudsonManagerPgRepository(session=db)
    return MrshudsonManagerInteractor(repository=repository)
