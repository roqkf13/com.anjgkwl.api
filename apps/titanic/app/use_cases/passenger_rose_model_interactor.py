from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from titanic.app.dtos.passenger_rose_model_dto import RoseIntroduction
from titanic.app.ports.input.passenger_rose_model_use_case import IntroduceRoseUseCase


class IntroduceRoseInteractor(IntroduceRoseUseCase):
    """자기소개 유스케이스 구현(영속성이 필요 없는 순수 로직)."""

    async def introduce(self, member_id: int, name: str) -> RoseIntroduction:
        return RoseIntroduction(
            id=member_id * 10000,
            name=f"{name}가 유스케이스에 다녀옴",
        )


class RoseModelService:
    """의사결정 나무 기반 생존 예측 모델(수업용). 유스케이스 포트와 별개의 ML 서비스."""

    def __init__(self) -> None:
        # 학습의 일관성을 위해 random_state를 지정합니다.
        self.model = DecisionTreeClassifier(random_state=42, max_depth=5)

    def get_model_name(self) -> str:
        return type(self.model).__name__

    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        """독립변수 X와 종속변수 y 데이터를 받아 의사결정 나무 모델 학습"""
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """주어진 입력 데이터 X에 대해 생존 여부(0 또는 1) 예측"""
        return self.model.predict(X)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """생존 및 사망에 대한 각각의 확률 반환"""
        return self.model.predict_proba(X)

    def get_accuracy(self, X: pd.DataFrame, y: pd.Series) -> float:
        """학습된 모델의 정확도 반환"""
        return float(self.model.score(X, y))
