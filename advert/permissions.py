from rest_framework import permissions

from advert.models import Advert
from user.models import User


class AdvertEditPermission(permissions.BasePermission):
    message = "You can't edit the advert"

    def has_permission(self, request, view):
        pk = view.kwargs.get('pk')
        author_id = Advert.objects.get(pk=pk).author.id
        if (request.user.id == author_id) | (request.user.role in (User.ADMIN, User.MODERATOR)):
            return True
        return False

