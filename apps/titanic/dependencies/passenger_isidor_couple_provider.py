from titanic.app.ports.input.passenger_isidor_couple_use_case import IntroduceIsidorUseCase
from titanic.app.use_cases.passenger_isidor_couple_interactor import IntroduceIsidorInteractor


def get_introduce_isidor_use_case() -> IntroduceIsidorUseCase:
    return IntroduceIsidorInteractor()
