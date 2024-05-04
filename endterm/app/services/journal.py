from pydantic import BaseModel

from app.kafka.producer import produce_journal_log


class JournalWriter:
    def write_journal(self, data: BaseModel, method: str, request: str):
        produce_journal_log({
            "data": data.model_dump(),
            "method": method,
            "request": request,
        })
