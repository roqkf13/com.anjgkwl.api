from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: str
    password: str
    email: str
    name: str
    role: str


