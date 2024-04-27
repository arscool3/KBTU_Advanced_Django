from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import mapped_column

default_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]
