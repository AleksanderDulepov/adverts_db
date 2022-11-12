import json

from django.conf import settings
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from advert.models import Advert
from advert.permissions import AdvertEditPermission
from advert.serializers import AdvertSerializer, AdvertCreateSerializer
from category.models import Category
from user.models import User



class AdvertListView(ListView):
    model = Advert

    def get(self, request, *args, **kwargs):

        # блок фильтрации
        data = request.GET
        self.queryset = self.get_queryset().select_related('author').select_related('category')

        category_list = data.getlist('cat')
        if category_list:
            self.queryset = self.queryset.filter(category__in=category_list)

        text = data.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = data.get('location')
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = data.get('price_from')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=int(price_from))

        price_to = data.get('price_to')
        if price_to:
            self.queryset = self.queryset.filter(price__lte=int(price_to))

        paginator = Paginator(self.queryset, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        advert_list = []
        for advert in page_obj:
            advert_list.append({"id": advert.id,
                                "name": advert.name,
                                "author_id": advert.author.id,
                                "price": advert.price,
                                "description": advert.description,
                                "is_published": advert.is_published,
                                "category_id": advert.category.id,
                                "image": advert.image.url if advert.image else None})

        response = {"items": advert_list, "num_pages": paginator.num_pages, "total": paginator.count}
        return JsonResponse(response)



# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
class AdvertDetailView(DetailView):
    model = Advert

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        advert = self.get_object()

        advert_dict = model_to_dict(advert, exclude=['image'])
        advert_dict["image"] = advert.image.url if advert.image else None

        return JsonResponse(advert_dict, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdvertCreateView(CreateView):
    model = Advert
    fields = list(model_to_dict(model, exclude=['id']).keys())

    def post(self, request, *args, **kwargs):
        data_dict = json.loads(request.body)
        advert = Advert(
            **{key: value for key, value in data_dict.items() if key not in ("id", "author", "category", "image")})

        # заполнение author вручную
        advert.author = get_object_or_404(User, pk=data_dict.get("author"))

        # заполнение category вручную
        advert.category = get_object_or_404(Category, pk=data_dict.get("category"))

        advert.save()

        # загрузка картинки сюда не идет, она отдельной ручкой на апдейте

        advert_dict = model_to_dict(advert, exclude=["image"])
        advert_dict["image"] = advert.image.url if advert.image else None
        return JsonResponse(advert_dict, status=201)





# @api_view(["PATCH"])
# @permission_classes([IsAuthenticated, AdvertEditPermission])
@method_decorator(csrf_exempt, name="dispatch")
class AdvertUpdateView(UpdateView):
    model = Advert
    fields = list(model_to_dict(model, exclude=['id']).keys())

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.queryset = self.get_queryset().filter(pk=self.object.id)
        data_dict = json.loads(request.body)

        self.queryset.update(
            **{key: value for key, value in data_dict.items() if key not in ("id", "author", "category", "image")})
        advert = self.get_object()

        # # заполнение author вручную
        if data_dict.get("author"):
            advert.author = get_object_or_404(User, pk=data_dict.get("author"))
        # заполнение category вручную
        if data_dict.get("category"):
            advert.category = get_object_or_404(Category, pk=data_dict.get("category"))

        # загрузка картинки сюда не идет, она отдельной ручкой на апдейте

        advert_dict = model_to_dict(advert, exclude=['image'])
        advert_dict["image"] = advert.image.url if advert.image else None
        return JsonResponse(advert_dict, status=204)




@method_decorator(csrf_exempt, name="dispatch")
class AdvertUpdateImageView(UpdateView):
    model = Advert
    fields = list(model_to_dict(model, exclude=['id']).keys())

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        # для оптимизации запросов advert.author.name, advert.category.id (джойним таблицы author и category)
        self.queryset = self.get_queryset().filter(pk=self.object.id).select_related('author').select_related(
            'category')

        advert = self.get_object()
        advert.image = request.FILES['image_for_adv']
        advert.save()

        return JsonResponse({"id": advert.id,
                             "name": advert.name,
                             "author_id": advert.author.id,
                             "author": advert.author.username,
                             "price": advert.price,
                             "description": advert.description,
                             "is_published": advert.is_published,
                             "category_id": advert.category.id,
                             "image": advert.image.url if advert.image else None}, status=204)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, AdvertEditPermission])
def delete(request, pk):
    if request.method == "DELETE":
        advert = get_object_or_404(Advert, pk=pk)
        advert.delete()
        return JsonResponse({"status":"ok"}, status=204)


# @method_decorator(csrf_exempt, name="dispatch")
# class AdvertDeleteView(DeleteView):
#     model = Advert
#     success_url = "/"
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#         return JsonResponse({"status": "ok"}, status=204)
