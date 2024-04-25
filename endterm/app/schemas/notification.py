from pydantic import BaseModel, Field

class NotificationBase(BaseModel):
    message: str

class NotificationCreate(NotificationBase):
    user_id: int = Field(..., title="User ID", description="The ID of the user to whom the notification is sent.")

class NotificationOut(NotificationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
