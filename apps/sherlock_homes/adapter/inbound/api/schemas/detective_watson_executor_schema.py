from pydantic import BaseModel, EmailStr, Field

'''
캐릭터: 존 왓슨 (John)
역할 (keyword): executor (실행/조율자)
드라마 설정 및 시스템 기능: 셜록의 파트너인 사설 탐정 조력자.
탐정의 추론 결과를 실제 현실 세계의 액션과 인간의 언어(블로그 등)로 번역하고 최종 사용자 인터페이스를 조율 및 실행합니다.
'''

class WatsonExecutorSchema(BaseModel):

    id: int = Field(0, description="존 왓슨 ID")
    name: str = Field("존 왓슨 (John)", description="셜록의 파트너, 추론 결과 실행 및 조율자")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 10,
                "name": "Watson executor",
            }
        }
    }


class WatsonSendEmailRequest(BaseModel):
    to: EmailStr = Field(..., description="수신자 이메일 주소")
    prompt: str = Field(..., description="EXAONE에 전달할 메일 작성 지시 (예: '채용 공고 지원서 요청 메일 작성')")
    from_account: EmailStr = Field(..., description="발신자 Gmail 계정")

    model_config = {
        "json_schema_extra": {
            "example": {
                "to": "recipient@example.com",
                "prompt": "프로젝트 일정 변경 안내 메일을 정중하게 작성해줘",
                "from_account": "sender@gmail.com",
            }
        }
    }
