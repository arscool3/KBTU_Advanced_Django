from database import session
from database.models import History
from core.schemas import HistoryOut, PersonOut

from .kwargs_searchers import get_user_by_kwargs


async def get_user_tracking_history(user_id: int) -> list[HistoryOut]:
    db_histories = session.query(History).filter_by(person_id=user_id).order_by(History.timestamps).all()
    return [HistoryOut.from_orm(db_history) for db_history in db_histories]


async def get_user_data(user_id: int) -> PersonOut:
    user = await get_user_by_kwargs(id=user_id)
    return PersonOut.model_validate(user)
