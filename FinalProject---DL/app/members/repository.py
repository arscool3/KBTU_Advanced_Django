from sqlalchemy.orm import Session

from app.models import Member
from app.members import schemas
from app.utils.repository import BaseRepository


class MemberRepo(BaseRepository):
    model = Member
    session = Session
    schema = schemas.Member
