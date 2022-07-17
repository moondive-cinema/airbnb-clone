import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models


class BookedDay(core_models.TimeStampedModel):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return str(self.day)


class Reservation(core_models.TimeStampedModel):

    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.room} - {str(self.check_in)}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    # admin 패널에서 in_progress의 표시가 "True/False"가 아니라 아이콘으로 나오게 한다
    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished

    # admin 패널에서 is_finished의 표시가 "True/False"가 아니라 아이콘으로 나오게 한다
    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects.filter(
                day__range=(start, end)
            ).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)
                for d in range(difference.days + 1):
                    day = start + datetime.timedelta(days=d)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)
