from multiprocessing import BoundedSemaphore
from django.views.generic import ListView, DetailView

# from django.http import Http404
from django_countries import countries
from django.shortcuts import render
from . import models


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"


class RoomDetail(DetailView):

    """Room Detail Definition"""

    model = models.Room


"""
# fbv version room detail

def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/room_detail.html", {"room": room})
    except models.Room.DoesNotExist:
        raise Http404()

"""


def search(request):
    city = request.GET.get("city", "anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    room_types = models.RoomType.objects.all()
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    beds = int(request.GET.get("beds", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    baths = int(request.GET.get("baths", 0))

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "beds": beds,
        "bedrooms": bedrooms,
        "baths": baths,
    }
    choices = {"countries": countries, "room_types": room_types}

    return render(
        request,
        "rooms/search.html",
        {**form, **choices},
    )
