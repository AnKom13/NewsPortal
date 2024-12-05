from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core.mail import mail_managers


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common = Group.objects.get(name="common")
        user.groups.add(common)

        # send_mail(
        #     subject='Добро пожаловать на новостной портал!',
        #     message=f'{user.username}, вы успешно зарегистрировались!',
        #     from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
        #     recipient_list=[user.email],
        # )

        subject = 'Привет'
        text = f'{user.username}, Вы успешно зарегистрировались на NewsPortal'
        html = (
            f'<b>{user.username}</b>, вы успешно ...'
            f'<a href="http://127.0.0.1:8000/pages">сайте</a>!'
        )
        print('=!=!=' * 10)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text,
            from_email=None,
            to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        print('==='*10)
        mail_managers(
            subject='Новый юзер',
            message=f'Юзер {user.username} зарегистрировался!'
        )
        return user


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
