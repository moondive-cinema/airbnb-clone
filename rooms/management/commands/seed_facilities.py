from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):

    help = "This command creates facilities"

    def handle(self, *args, **options):

        STUFF = "facilities"

        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        for item_f in facilities:
            Facility.objects.create(name=item_f)
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} {STUFF} created!"))
