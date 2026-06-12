from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str = Field(..., description="user 또는 assistant")
    text: str = Field(..., description="메시지 내용")


class ChatSchema(BaseModel):
    messages: list[ChatMessage] = Field(..., description="대화 히스토리")

    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [
                    {"role": "user", "text": "선장님, 빙산 경고를 받으셨나요?"}
                ]
            }
        }
    }

class SmithCaptainSchema(BaseModel):

    id: int = Field(0, description="Captain ID")
    name: str = Field("에드워드 스미스", description="Captain's name")
    # 타이타닉 선장. 백만장자들의 선장이라 불렸으며 고조되는 위기 속에 배와 운명을 함께함

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Edward Smith",
            }
        }
    }