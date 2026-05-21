import logging

from sklearn.tree import DecisionTreeClassifier

from titanic.app.repositories.rose_repository import RoseRepository
from titanic.app.repositories.walter_repository import WalterRepository

logger = logging.getLogger(__name__)


class JackService:
    """타이타닉 데이터 로드·모델 학습 조율."""

    def __init__(
        self,
        walter: WalterRepository,
        rose: RoseRepository,
    ) -> None:
        self.walter = walter
        self.rose = rose
        self._ensure_trained()

    def _ensure_trained(self) -> None:
        frame = self.walter.get_training_frame()
        self.rose.train(frame)
        logger.info("[JackService] 모델 학습 파이프라인 완료")

    def get_model_name_and_accuracy(self) -> dict[str, str | float]:
        return self.rose.get_model_name_and_accuracy()

    def has_decision_tree_model(self) -> bool:
        return isinstance(self.rose.model, DecisionTreeClassifier)
