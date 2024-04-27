from settings import celery_app


@celery_app.task
def perform(x, y):
    return x + y
