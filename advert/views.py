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
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from advert.models import Advert
from advert.permissions import AdvertEditPermission
from advert.serializers import AdvertSerializer, AdvertCreateSerializer
from category.models import Category
from user.models import User

class AdvertListView(ListAPIView):
    queryset=Advert.objects.all()
    serializer_class=AdvertSerializer

class AdvertDetailView(RetrieveAPIView):
    queryset=Advert.objects.all()
    serializer_class=AdvertSerializer
    permission_classes=[IsAuthenticated]

class AdvertCreateView(CreateAPIView):
    queryset=Advert.objects.all()
    serializer_class=AdvertCreateSerializer

class AdvertUpdateView(UpdateAPIView):
    queryset=Advert.objects.all()
    serializer_class=AdvertSerializer


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

class AdvertDeleteView(DestroyAPIView):
    queryset=Advert.objects.all()
    serializer_class=AdvertSerializer
    permission_classes=[IsAuthenticated, AdvertEditPermission]

