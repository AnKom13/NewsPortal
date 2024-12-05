import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from ...models import Post, PostCategory, Category

logger = logging.getLogger(__name__)


def weekly_newsletter():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=27)
    articles = Post.objects.filter(property__exact='N').filter(time_create__gte=last_week)
    categories = set(articles.values_list('category__name', flat=True))
    emails_ = set(Category.objects.filter(name__in=categories).values_list('subscriber__user__email', flat=True))
    emails = [x for x in emails_ if x is not None]

    for email in emails:
        articles_personal = articles.filter(category__subscriber__user__email=email)
        html_content = render_to_string(
            'weekly_post.html',
            {
                'link': settings.SITE_URL,
                'posts': articles_personal,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Новые статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        #    print(categories)
        #    articles_personal = articles.filter(category__subscriber__user__email='b@list.ru')
        #    print(articles_personal)

        msg.attach_alternative(html_content, 'text/html')

        msg.send()


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_newsletter,
            #            trigger=CronTrigger(second="*/15"), #каждые 15 сек.
            trigger=CronTrigger(day_of_week='mon', hour='00', minute='00'),
            id="weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Недельная рассылка: 'weekly_newslette'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
