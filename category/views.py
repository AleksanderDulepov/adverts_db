import json

from django.conf import settings
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from category.models import Category


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
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        data_dict = json.loads(request.body)
        category = Category.objects.create(**{key: value for key, value in data_dict.items() if key not in ("id")})

        category_dict = model_to_dict(category)
        return JsonResponse(category_dict, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data_dict = json.loads(request.body)
        self.object.name = data_dict.get("name")
        self.object.save()
        category_dict = model_to_dict(self.object)
        return JsonResponse(category_dict, status=204)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=204)
