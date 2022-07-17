from django.contrib import admin
from django.utils import timezone
from . import models


class ProgressListFilter(admin.SimpleListFilter):

    """In Progress Filter Definition"""

    title = "In Progress"
    parameter_name = "in_progress"

    def lookups(self, request, model_admin):
        return (("True", "True"), ("False", "False"))

    def queryset(self, request, queryset):
        now = timezone.localdate()
        if self.value() == "True":
            return queryset.filter(check_in__lte=now, check_out__gte=now)
        else:
            return queryset.exclude(check_in__lte=now, check_out__gte=now)


class FinishedListFilter(admin.SimpleListFilter):

    """Finished Status Filter Definition"""

    title = "Is Finished"
    parameter_name = "is_finished"

    def lookups(self, request, model_admin):
        return (("True", "True"), ("False", "False"))

    def queryset(self, request, queryset):
        now = timezone.localdate()
        if self.value() == "True":
            return queryset.filter(check_out__lt=now)
        else:
            return queryset.exclude(check_out__lt=now)


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """Reservation Admin Definition"""

    list_display = (
        "room",
        "check_in",
        "check_out",
        "status",
        "guest",
        "in_progress",
        "is_finished",
    )

    # list_filter = ("status", ProgressListFilter, FinishedListFilter)


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):

    list_display = (
        "day",
        "reservation",
    )
