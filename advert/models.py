from django.db import models

from category.models import Category
from user.models import User


class Advert(models.Model):
    name = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name
