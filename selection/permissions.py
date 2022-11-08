from rest_framework import permissions


class SelectionEditPermission(permissions.BasePermission):
    message = "Editing, removing selections is allowed only for owners"

    def has_permission(self, request, view):
        if request.user.id == view.get_object().owner_id:
            return True
        return False