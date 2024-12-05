from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import PostCategory



@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    categories = instance.category.all()
    subs: list[str] = []
    title_category = ''
    for c in categories:
        subs += c.subscriber.all()
        title_category += f' -> {c.name}'

    emails = set([s.user.email for s in subs])


    subject = f'Новый пост в категории {title_category}'

    text_content = (
        f'Тип: {instance.property}\n'
        f'Заголовок: {instance.heading}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )

    html_content = (
        f'Тип: {instance.property}<br>'
        f'Заголовок: {instance.heading}<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )

    for email in emails:
        # можно БЫЛО БЫ сразу дать список мыл, но тогда каждый получатель увидит мыло всех кому отправлено
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

