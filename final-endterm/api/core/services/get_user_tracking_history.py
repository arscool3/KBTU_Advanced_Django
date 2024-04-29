from database import session
from database.models import History
from core.schemas import HistoryOut


async def get_user_tracking_history(user_id: int) -> list[HistoryOut]:
    db_histories = session.query(History).filter_by(person_id=user_id).order_by(History.timestamps).all()
    return [HistoryOut.from_orm(db_history) for db_history in db_histories]
