import dramatiq
from dramatiq.results.backends.redis import RedisBackend
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results, ResultMissing
import models as db
from database import get_db

result_backend = RedisBackend()
broker = RedisBroker()
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)


@dramatiq.actor
def change_budget(amount: float, project_id: int):
    print(" I am changing the  budget")
    with get_db() as session:
        project = session.query(db.Project).filter_by(id=project_id).first()
        project.current_budget -= amount


@dramatiq.actor
def project_fatality(project_id: int):
    with get_db() as session:
        project = session.query(db.Project).filter_by(id=project_id).first()
        project.is_finished = True
        print(project.is_finished)
        organization = session.query(db.Organization).filter_by(id=project.organization_id).first()
        organization.num_of_finished_projects += 1
        session.commit()