from django.contrib.auth.models import AbstractUser
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=150, unique=True)
    lat=models.FloatField(null=True, blank=True)
    lng=models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
            return self.name


ROLES = [("admin", "Администратор"), ("moderator", "Модератор"), ("member", "Участник")]
class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLES, default="member",null=True)
    age = models.IntegerField(null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username

