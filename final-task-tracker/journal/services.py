from pydantic import BaseModel

from journal.producer import produce_journal_message


class JournalWriter:

    def write_journal(self, data: BaseModel, method: str, request: str, user_id: int):
        produce_journal_message({
            "data": data.model_dump(),
            "method": method,
            "request": request,
            "user_id": user_id,
        })