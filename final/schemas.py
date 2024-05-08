from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class CreateProfileRequest(BaseModel):
    education: str
    experience: int
    stack: str
    current_workplace: str
    coverletter: str
    user_id: int


