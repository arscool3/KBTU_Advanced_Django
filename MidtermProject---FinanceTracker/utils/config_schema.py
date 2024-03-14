from pydantic import BaseModel


class ConfigSchema(BaseModel):
    class Config:
        from_attributes = True
