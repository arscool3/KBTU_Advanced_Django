from pydantic import BaseModel


class BaseSchema(BaseModel):

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
