from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from knox.auth import TokenAuthentication
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import generics, status
from . import models
from . import serializers
from rest_framework import filters
from django.db.models import Q
from modules.business.sponsoring import models as SponsorModels
from modules.business.sponsoring import serializers as SponsorSerializers
from modules.utilities.users_management import permissions

class ListLocals(generics.ListCreateAPIView):
    queryset = models.Local.objects.all()
    serializer_class = serializers.LocalSerializer
    filter_backends = [filters.SearchFilter]

    def get_permissions(self):
        return super().get_permissions()
    

class CreateActivity(generics.CreateAPIView):
    queryset = SponsorModels.Activity.objects.all()
    serializer_class = SponsorSerializers.ActivitySerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsDonkeyProvider, permissions.IsLocalOwner]

    def perform_create(self, serializer):
        serializer.save()