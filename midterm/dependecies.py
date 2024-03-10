from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated
from database import get_db

Database = Annotated[Session, Depends(get_db)]
