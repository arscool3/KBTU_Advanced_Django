import csv
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from journal.models import Journal
from users.models import User


class CSVReportCreator:
    def __init__(self, session: Session, request_user: User):
        self.session = session
        self.request_user = request_user

    def create_report(self) -> str:
        access_logs = self.session.execute(select(Journal)).scalars().all()
        filename = self._get_filename()
        with open(f"./shared_storage/reports/{filename}", "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Journal ID", "Method", "Request", "Time", "User", "Data"])
            for log in access_logs:
                writer.writerow(
                    [
                        log.id,
                        log.method,
                        log.request,
                        log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        log.user_id,
                        log.data,
                    ]
                )
        return filename

    def _get_filename(self):
        return (f"{self.request_user.first_name}_{self.request_user.last_name}_"
                f"{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.csv")
