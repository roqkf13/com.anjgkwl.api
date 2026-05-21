from pathlib import Path

import pandas as pd

from titanic.app.schemas.titanic_problem_schema import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
)

_CSV_PATH = Path(__file__).resolve().parent.parent / "Titanic-Dataset.csv"


class WalterRepository:
    """타이타닉 CSV(탑승자 명단) 읽기."""

    def get_data(self) -> pd.DataFrame:
        return pd.read_csv(_CSV_PATH)

    def get_training_frame(self) -> pd.DataFrame:
        df = self.get_data()
        columns = [TARGET_COLUMN, *FEATURE_COLUMNS]
        return df[columns].copy()

    def get_count(self) -> int:
        return int(self.get_data().shape[0])

    def get_count_survived(self) -> int:
        df = self.get_data()
        return int((df[TARGET_COLUMN] == 1).sum())

    def get_count_dead(self) -> int:
        df = self.get_data()
        return int((df[TARGET_COLUMN] == 0).sum())
