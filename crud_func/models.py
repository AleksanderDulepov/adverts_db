from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)


class Advert(models.Model):
    name = models.TextField()
    author = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    address = models.TextField()
    is_published = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
