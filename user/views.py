import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Exists, Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from advert.models import Advert
from user.models import User, Location


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related('location').annotate(
            total_adverts=Count('advert', filter=Q(advert__is_published=True))).order_by("username")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        user_list = []
        for user in page_obj:
            user_list.append({"id": user.id,
                              "username": user.username,
                              "first_name": user.first_name,
                              "last_name": user.last_name,
                              "role": user.role,
                              "age": user.age,
                              "location": user.location.name if user.location else None,  # могут быть юзеры без адреса
                              "total_adverts": user.total_adverts
                              })

        response = {"items": user_list, "num_pages": paginator.num_pages, "total": paginator.count}

        return JsonResponse(response)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.queryset = self.get_queryset().filter(pk=self.object.id).select_related('location').annotate(
            total_adverts=Count('advert', filter=Q(advert__is_published=True)))

        user = self.get_object()

        user_dict = model_to_dict(user, exclude=['location'])
        user_dict["location"] = user.location.name if user.location else None  # могут быть юзеры без адреса
        user_dict["total_adverts"] = user.total_adverts

        return JsonResponse(user_dict, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["id", "username", "password"]

    def post(self, request, *args, **kwargs):
        data_dict = json.loads(request.body)
        user = User(**{key: value for key, value in data_dict.items() if key not in ("id", "location")})

        # заполнение/создание location
        if data_dict.get("location"):
            location_obj, created = Location.objects.get_or_create(name=data_dict.get("location"))
            user.location = location_obj

        user.save()

        user_dict = model_to_dict(user, exclude=['location'])
        user_dict["location"] = user.location.name if user.location else None  # могут быть юзеры без адреса

        return JsonResponse(user_dict, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ["id", "username", "password"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.queryset = self.get_queryset().filter(pk=self.object.id).select_related('location')
        data_dict = json.loads(request.body)

        self.queryset.update(**{key: value for key, value in data_dict.items() if key not in ("id", "location")})
        user = self.get_object()

        # заполнение/создание location
        if data_dict.get("location"):
            location_obj, created = Location.objects.get_or_create(name=data_dict.get("location"))
            user.location = location_obj

        user.save()

        user_dict = model_to_dict(user, exclude=['location'])
        user_dict["location"] = user.location.name if user.location else None

        return JsonResponse(user_dict, status=204)


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=204)
