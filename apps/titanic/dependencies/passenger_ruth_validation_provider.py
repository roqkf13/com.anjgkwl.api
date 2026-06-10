from titanic.app.ports.input.passenger_ruth_validation_use_case import IntroduceRuthUseCase
from titanic.app.use_cases.passenger_ruth_validation_interactor import IntroduceRuthInteractor


def get_introduce_ruth_use_case() -> IntroduceRuthUseCase:
    return IntroduceRuthInteractor()
