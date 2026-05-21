"""타이타닉 생존 예측 — 이진 분류 문제 정의."""

# 종속변수(라벨): Survived (0=사망, 1=생존)
TARGET_COLUMN = "Survived"

# 독립변수 6개 — 승객 특성으로 생존 유무 예측
FEATURE_COLUMNS = ("Pclass", "Sex", "Age", "SibSp", "Parch", "Fare")

# 데이터셋 메타·부가 컬럼(모델 입력 제외, 분석·검증용)
PASSENGER_META_COLUMNS = ("PassengerId", "Name", "Ticket", "Cabin", "Embarked")

PROBLEM_SUMMARY = (
    "1912년 타이타닉 탑승자 명단으로 생존자 이진 분류를 수행한다. "
    "독립변수 6개(Pclass, Sex, Age, SibSp, Parch, Fare)로 "
    "Survived(0=사망, 1=생존)를 예측한다."
)
