import datetime

from celery import shared_task

import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings
#from NewsPortal.NewsPortal import settings
from .models import Post, Category


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
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