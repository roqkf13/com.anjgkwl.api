from dataclasses import dataclass

'''
캐릭터: 메리 왓슨 (Mary)
역할 (keyword): operator (특수 작전/보안)
드라마 설정 및 시스템 기능: 사설 탐정단에 합류한 전직 비밀 요원.
베이커가 팀의 안전을 도모하듯, 시스템 내부의 예외 처리(Exception), 보안 우회 로직 및 긴급 특수 작전 코드를 수행합니다.
'''

@dataclass(frozen=True)
class MaryOperatorQuery:
    id: int
    name: str


@dataclass(frozen=True)
class MaryOperatorResponse:
    id: int
    name: str
