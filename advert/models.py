from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from category.models import Category
from user.models import User


class Advert(models.Model):
    name=models.TextField(null=False, validators=[MinLengthValidator(10, "Значение не может быть менее 10 символов")])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price=models.IntegerField(validators=[MinValueValidator(0)])
    description=models.TextField(null=True)
    is_published=models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name
