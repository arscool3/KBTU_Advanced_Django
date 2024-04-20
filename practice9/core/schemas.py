import pydantic
from datetime import datetime


class HeatMap(pydantic.BaseModel):
    time: datetime
    data: dict

    class Config:
        from_attributes = True