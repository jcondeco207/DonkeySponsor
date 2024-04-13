from rest_framework import permissions
from . import models

class IsDonkeyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role.name == 'DonkeyAdmin'
