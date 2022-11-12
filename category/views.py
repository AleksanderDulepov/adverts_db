import json

from django.conf import settings
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import CreateAPIView, UpdateAPIView

from category.models import Category
from category.serializers import CategorySerializer


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        category_list = [model_to_dict(category) for category in page_obj]
        response = {"items": category_list, "num_pages": paginator.num_pages, "total": paginator.count}

        return JsonResponse(response)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse(model_to_dict(category), status=200)

@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(UpdateView):
    model = Category
    fields = ['name']



class CategoryCreateView(CreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class CategoryUpdateView(UpdateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=204)
