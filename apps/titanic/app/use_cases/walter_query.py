from __future__ import annotations

import pandas as pd

from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.ports.output.walter_repository import WalterRepository


class WalterQuery(WalterUseCase):
    def __init__(self, repository: WalterRepository) -> None:
        self._repository = repository

    async def get_titanic_data(self) -> pd.DataFrame:
        rows = await self._repository.get_data()
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows)

    async def get_titanic_data_count(self) -> int:
        return await self._repository.get_count()

    async def get_titanic_data_count_survived(self) -> int:
        return await self._repository.get_count_survived()

    async def get_titanic_data_count_dead(self) -> int:
        return await self._repository.get_count_dead()
