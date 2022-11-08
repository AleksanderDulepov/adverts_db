from django.db import models

from advert.models import Advert
from user.models import User


class Selection(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              verbose_name="Автор подборки",
                              related_name="selection_author"
                              )
    items = models.ManyToManyField(Advert,
                              verbose_name="Список обьявлений",
                              related_name="adverts_list"
                              )
