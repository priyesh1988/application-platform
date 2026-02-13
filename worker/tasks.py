from worker.celery_app import celery_app

@celery_app.task
def dummy_task():
    return {"status": "ok"}

