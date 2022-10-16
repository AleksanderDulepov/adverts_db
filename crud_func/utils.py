import csv

from django.forms import model_to_dict
from django.http import JsonResponse

from crud_func.models import Advert, Category


def load_universal(path: str, model):
    with open(path, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        first_line = list(reader.__next__())
        values_indexes = {}
        values_list = list(model_to_dict(model, exclude=['id']).keys())
        try:
            for value in values_list:
                values_indexes[value] = first_line.index(value)
        except IndexError:
            return JsonResponse({"error": f"CSV file is not valid"}, status=404)
        for line in reader:
            instance = model()
            for key, value in values_indexes.items():
                if key != "category":
                    setattr(instance, key, line[value])
                else:
                    category = Category.objects.get(id=line[value]) if Category.objects.filter(
                        id=line[value]).exists() else None
                    setattr(instance, key, category)
            instance.save()
