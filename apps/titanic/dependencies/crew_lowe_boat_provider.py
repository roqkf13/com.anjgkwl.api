from titanic.app.ports.input.crew_lowe_boat_use_case import IntroduceLoweUseCase
from titanic.app.use_cases.crew_lowe_boat_interactor import IntroduceLoweInteractor


def get_introduce_lowe_use_case() -> IntroduceLoweUseCase:
    return IntroduceLoweInteractor()
