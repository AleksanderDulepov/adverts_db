import json
from typing import List, Dict

from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.views.generic.detail import DetailView

from advert.models import Advert
from category.models import Category


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        categories_list: List[Dict] = [model_to_dict(category) for category in categories]
        return JsonResponse(categories_list, safe=False)

    def post(self, request, *args, **kwargs):
        data_dict = json.loads(request.body)
        category = Category()
        category.name = data_dict.get("name")
        category.save()
        category_dict = model_to_dict(category)
        return JsonResponse(category_dict)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse(model_to_dict(category))


@method_decorator(csrf_exempt, name="dispatch")
class AdvertView(View):
    def get(self, request, *args, **kwargs):
        adverts = Advert.objects.all()
        adverts_list: List[Dict] = [model_to_dict(advert) for advert in adverts]
        return JsonResponse(adverts_list, safe=False)

    def post(self, request, *args, **kwargs):
        data_dict = json.loads(request.body)
        advert = Advert(**{key: value for key, value in data_dict.items() if key != "category"})
        advert.category = Category.objects.get(id=data_dict.get('category')) if Category.objects.filter(
            id=data_dict.get('category')).exists() else None
        advert.save()
        advert_dict = model_to_dict(advert)
        return JsonResponse(advert_dict)


class AdvertDetailView(DetailView):
    model = Advert

    def get(self, request, *args, **kwargs):
        advert = self.get_object()
        return JsonResponse(model_to_dict(advert))

