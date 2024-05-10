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


class CreateProjectRequest(BaseModel):
    title: str
    description: str
    github_link: str
    creator_id: int


class UpdateProjectRequest(BaseModel):
    title: str
    desciprion: str
    github_link: str


class CreatePostRequest(BaseModel):
    title: str
    description: str
    author_id: str


class UpdatePostRequest(BaseModel):
    title: str
    description: str


class KafkaRequest(BaseModel):
    project_id: int
    user_id: int
