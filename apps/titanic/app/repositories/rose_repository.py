import logging

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from titanic.app.models.rose_model import RoseModel
from titanic.app.schemas.titanic_problem_schema import FEATURE_COLUMNS, TARGET_COLUMN

logger = logging.getLogger(__name__)


class RoseRepository:
    """RoseModel 학습·평가(레포지토리)."""

    def __init__(self) -> None:
        self._rose = RoseModel()
        self._accuracy: float | None = None

    @property
    def model(self) -> DecisionTreeClassifier:
        return self._rose.model

    def _prepare_xy(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        work = df.copy()
        work["Sex"] = work["Sex"].map({"male": 0, "female": 1})
        work["Age"] = work["Age"].fillna(work["Age"].median())
        for col in ("Pclass", "SibSp", "Parch", "Fare"):
            work[col] = work[col].fillna(work[col].median())
        x = work[list(FEATURE_COLUMNS)]
        y = work[TARGET_COLUMN]
        return x, y

    def train(self, df: pd.DataFrame) -> None:
        x, y = self._prepare_xy(df)
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42, stratify=y
        )
        self._rose.model.fit(x_train, y_train)
        self._accuracy = float(self._rose.model.score(x_test, y_test))
        logger.info(
            "[RoseRepository] train 완료 — model=%s accuracy=%.4f",
            self._rose.get_model_name(),
            self._accuracy,
        )

    def get_model_name_and_accuracy(self) -> dict[str, str | float]:
        return {
            "model_name": self._rose.get_model_name(),
            "accuracy": self._accuracy if self._accuracy is not None else 0.0,
            "target": TARGET_COLUMN,
            "features": list(FEATURE_COLUMNS),
        }
