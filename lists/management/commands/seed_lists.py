import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.admin.utils import flatten
from lists import models as list_models
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates lists"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many lists you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(users)}
        )

        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            sample_k = random.randint(0, len(rooms))
            if sample_k > 10:
                sample_k = 10 + (sample_k % 10)
            to_add = random.sample(list(rooms), sample_k)
            list_model.rooms.add(
                *to_add
            )  # to_add만 쓰면 array가 추가 되고 *을 앞에 서줘서 array의 요소들이 추가되게 함

        self.stdout.write(self.style.SUCCESS(f"{number} lists created!"))
