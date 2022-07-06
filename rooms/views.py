from django.views.generic import ListView, DetailView, View

# from django.http import Http404
# from django_countries import countries
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 8
    paginate_orphans = 5
    ordering = "created"


class RoomDetail(DetailView):

    """Room Detail Definition"""

    model = models.Room


class SearchView(View):

    """Search View Definition"""

    def get(self, request):

        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__contains"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["superhost"] = True

                if amenities is not None:
                    for amenity in amenities:
                        filter_args["amenities"] = amenity

                if facilities is not None:
                    for facility in facilities:
                        filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")
                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


"""
# fbv version room detail

def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/room_detail.html", {"room": room})
    except models.Room.DoesNotExist:
        raise Http404()


# search function building from the scratch version

def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    beds = int(request.GET.get("beds", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    checked_amenities = request.GET.getlist("amenities")
    checked_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "beds": beds,
        "bedrooms": bedrooms,
        "baths": baths,
        "instant": instant,
        "superhost": superhost,
        "checked_amenities": checked_amenities,
        "checked_facilities": checked_facilities,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__contains"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant"] = True

    if superhost is True:
        filter_args["superhost"] = True

    if len(checked_amenities) > 0:
        for amenity_pk in checked_amenities:
            filter_args["amenities__pk"] = int(amenity_pk)

    if len(checked_facilities) > 0:
        for facility_pk in checked_facilities:
            filter_args["facilities__pk"] = int(facility_pk)

    rooms = models.Room.objects.filter(**filter_args)

    return render(
        request,
        "rooms/search.html",
        {**form, **choices, "rooms": rooms},
    )
"""
