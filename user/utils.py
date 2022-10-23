import csv

from django.forms import model_to_dict
from django.http import JsonResponse

from category.models import Category
from user.models import User, Location


def load_universal(path: str, model):
    with open(path, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        first_line = list(reader.__next__())
        values_indexes = {}
        if model==User:
            values_list = ["first_name","last_name","username","password","role","age","location"]
        else:
            values_list = list(model_to_dict(model, exclude=['id']).keys())
        try:
            for value in values_list:
                values_indexes[value] = first_line.index(value)
        except IndexError:
            return JsonResponse({"error": f"CSV file is not valid"}, status=404)
        for line in reader:
            instance = model()
            for key, value in values_indexes.items():
                if key == "location":
                    location = Location.objects.get(id=line[value]) if Location.objects.filter(
                        id=line[value]).exists() else None
                    setattr(instance, f"{key}_id", location.id)
                elif key == "category":
                    category = Category.objects.get(id=line[value]) if Category.objects.filter(
                        id=line[value]).exists() else None
                    setattr(instance, f"{key}_id", category.id)
                elif key == "author":
                    author = User.objects.get(id=line[value]) if User.objects.filter(
                        id=line[value]).exists() else None
                    setattr(instance, f"{key}_id", author.id)
                else:
                    setattr(instance, key, line[value])

            instance.save()
