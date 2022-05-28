from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other")
    )

    LANGUAGE_KOREAN = "kr"
    LANGUAGE_ENGLISH = "en"

    LANGUAGE_CHOICES = (
        (LANGUAGE_KOREAN, "Korean"),
        (LANGUAGE_ENGLISH, "English")
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRNECY_CHOICES = (
        (CURRENCY_KRW, "KRW"),
        (CURRENCY_USD, "USD")
    )

    avatar = models.ImageField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    birthdate = models.DateField(null=True)
    bio = models.TextField(default="", max_length=150, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=3, null=True, blank=True)
    currency = models.CharField(choices=CURRNECY_CHOICES, max_length=3, null=True, blank=True)
    superhost = models.BooleanField(default=False)
