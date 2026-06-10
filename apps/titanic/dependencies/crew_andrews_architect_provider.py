from titanic.app.ports.input.crew_andrews_architect_use_case import IntroduceAndrewsUseCase
from titanic.app.use_cases.crew_andrews_architect_interactor import IntroduceAndrewsInteractor


def get_introduce_andrews_use_case() -> IntroduceAndrewsUseCase:
    return IntroduceAndrewsInteractor()
