from django.db import models


class TimeStampedModel:

    """ Time Stamped Model """

    created = models.DateField(auto_now_add=True)
    upadated = models.DateField(auto_now=True)

    class Meta:
        abstract = True