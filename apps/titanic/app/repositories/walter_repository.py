import pandas as pd

from titanic.app.schemas.titanic_problem_schema import (
    PASSENGER_META_COLUMNS,
    FEATURE_COLUMNS,
    TARGET_COLUMN,
)

_TITANIC_ROWS: list[dict[str, object]] = [
    {
        "PassengerId": 1,
        "Name": "Allen, Miss. Elisabeth",
        "Ticket": "A/5 21171",
        "Cabin": "C85",
        "Embarked": "S",
        "Pclass": 1,
        "Sex": "female",
        "Age": 29.0,
        "SibSp": 0,
        "Parch": 0,
        "Fare": 82.1708,
        "Survived": 1,
    },
    {
        "PassengerId": 2,
        "Name": "Moran, Mr. James",
        "Ticket": "330877",
        "Cabin": "",
        "Embarked": "Q",
        "Pclass": 3,
        "Sex": "male",
        "Age": 24.0,
        "SibSp": 0,
        "Parch": 0,
        "Fare": 8.4583,
        "Survived": 0,
    },
    {
        "PassengerId": 3,
        "Name": "Johnson, Mrs. Oscar",
        "Ticket": "113803",
        "Cabin": "C123",
        "Embarked": "S",
        "Pclass": 1,
        "Sex": "female",
        "Age": 35.0,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 53.1,
        "Survived": 1,
    },
    {
        "PassengerId": 4,
        "Name": "Palsson, Master. Gosta",
        "Ticket": "349909",
        "Cabin": "",
        "Embarked": "S",
        "Pclass": 3,
        "Sex": "male",
        "Age": 2.0,
        "SibSp": 3,
        "Parch": 1,
        "Fare": 21.075,
        "Survived": 0,
    },
    {
        "PassengerId": 5,
        "Name": "Futrelle, Mrs. Jacques",
        "Ticket": "113803",
        "Cabin": "B49",
        "Embarked": "S",
        "Pclass": 1,
        "Sex": "female",
        "Age": 37.0,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 53.1,
        "Survived": 1,
    },
    {
        "PassengerId": 6,
        "Name": "Rice, Master. Eugene",
        "Ticket": "382652",
        "Cabin": "",
        "Embarked": "S",
        "Pclass": 3,
        "Sex": "male",
        "Age": 2.0,
        "SibSp": 4,
        "Parch": 1,
        "Fare": 29.125,
        "Survived": 0,
    },
    {
        "PassengerId": 7,
        "Name": "Harper, Mrs. Henry",
        "Ticket": "PC 17572",
        "Cabin": "D33",
        "Embarked": "C",
        "Pclass": 1,
        "Sex": "female",
        "Age": 49.0,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 76.7292,
        "Survived": 1,
    },
    {
        "PassengerId": 8,
        "Name": "Skoog, Mr. Wilhelm",
        "Ticket": "347088",
        "Cabin": "",
        "Embarked": "S",
        "Pclass": 3,
        "Sex": "male",
        "Age": 40.0,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 9.475,
        "Survived": 0,
    },
    {
        "PassengerId": 9,
        "Name": "Bonnell, Miss. Elizabeth",
        "Ticket": "113783",
        "Cabin": "C103",
        "Embarked": "S",
        "Pclass": 1,
        "Sex": "female",
        "Age": 58.0,
        "SibSp": 0,
        "Parch": 0,
        "Fare": 26.55,
        "Survived": 1,
    },
    {
        "PassengerId": 10,
        "Name": "Andersson, Mr. Anders",
        "Ticket": "347082",
        "Cabin": "",
        "Embarked": "S",
        "Pclass": 3,
        "Sex": "male",
        "Age": 39.0,
        "SibSp": 1,
        "Parch": 5,
        "Fare": 31.275,
        "Survived": 0,
    },
    {
        "PassengerId": 11,
        "Name": "Chambers, Mrs. Norman",
        "Ticket": "113806",
        "Cabin": "E8",
        "Embarked": "S",
        "Pclass": 1,
        "Sex": "female",
        "Age": 33.0,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 80.0,
        "Survived": 1,
    },
    {
        "PassengerId": 12,
        "Name": "Panula, Master. Eino",
        "Ticket": "3101295",
        "Cabin": "",
        "Embarked": "S",
        "Pclass": 3,
        "Sex": "male",
        "Age": 1.0,
        "SibSp": 4,
        "Parch": 1,
        "Fare": 39.6875,
        "Survived": 0,
    },
]


class WalterRepository:
    """타이타닉 탑승자 명단을 인메모리 데이터셋으로 제공."""

    def get_data(self) -> pd.DataFrame:
        columns = [*PASSENGER_META_COLUMNS, *FEATURE_COLUMNS, TARGET_COLUMN]
        return pd.DataFrame(_TITANIC_ROWS, columns=columns)

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
