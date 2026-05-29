from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class WalterQueryPort(ABC):
    @abstractmethod
    async def get_titanic_data(self) -> pd.DataFrame:
        ...

    @abstractmethod
    async def get_titanic_data_count(self) -> int:
        ...

    @abstractmethod
    async def get_titanic_data_count_survived(self) -> int:
        ...

    @abstractmethod
    async def get_titanic_data_count_dead(self) -> int:
        ...
