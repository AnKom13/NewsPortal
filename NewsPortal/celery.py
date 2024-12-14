from celery.schedules import crontab
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

#app = Celery('NewsPortal')
app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_articles_every_monday_8:00': {
        'task': 'news.tasks.weekly_newsletter',
        'schedule': crontab(day_of_week='monday', minute=0, hour=8),
        # раз в минуту         'schedule': crontab(),
    },
}
