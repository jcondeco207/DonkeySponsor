from rest_framework import permissions
from . import models
from modules.business.local_management import models as LocalsModels

class IsDonkeyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role.name == 'DonkeyAdmin'


class IsDonkeyGodFather(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role.name == 'DonkeyGodFather'
    
class IsDonkeyProvider(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role.name == 'DonkeyProvider'

class IsNotDonkeyProvider(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role.name != 'DonkeyProvider'

class IsDonkeyOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

class IsLocalOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        localId = view.kwargs.get('local_id', None)
        if not localId:
            return False
        local = LocalsModels.Local.objects.get(id=localId)
        return local.owner == request.user
