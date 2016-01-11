from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

'''
Planificateur de tâches.

Import le planificateur avec from app.outils.planification import scheduler
'''

scheduler = BackgroundScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(url=app.config['SQLALCHEMY_DATABASE_URI'])
    },
    job_defaults={
        'coalesce': True
    },
    timezone=utc
)

scheduler.start()