from titanic.app.ports.input.crew_smith_captain_use_case import IntroduceSmithUseCase
from titanic.app.use_cases.crew_smith_captain_interactor import IntroduceSmithInteractor


def get_introduce_smith_use_case() -> IntroduceSmithUseCase:
    return IntroduceSmithInteractor()
