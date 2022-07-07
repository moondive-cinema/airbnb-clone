import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.shortcuts import reverse


class User(AbstractUser):

    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_KOREAN = "kr"
    LANGUAGE_ENGLISH = "en"

    LANGUAGE_CHOICES = ((LANGUAGE_KOREAN, "Korean"), (LANGUAGE_ENGLISH, "English"))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_KRW, "KRW"), (CURRENCY_USD, "USD"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    """
    유저네임을 이메일로 받기 위한 코드 스니펫
    검증 필요. 빠르게 테스트 해봤을 때는 작동하지 않았음.

    USERNAME_FIELD = "email"
    email = models.EmailField(('email address'), unique=True)
    REQUIRED_FIELDS = []
    """

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=400, blank=True, default="")
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=3, blank=True, default="LANGUAGE_KOREAN"
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default="CURRENCY_KRW"
    )
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_key = models.CharField(max_length=20, default="", blank=True)
    login_method = models.CharField(
        max_length=40, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})


    def verify_email(self):
        if self.email_verified is False:
            key = uuid.uuid4().hex[:20]
            self.email_key = key
            html_message = render_to_string("emails/verify_email.html", {"key"})
            send_mail(
                "Verify Email",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        else:
            return
