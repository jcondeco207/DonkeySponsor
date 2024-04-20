from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from knox.auth import TokenAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework import generics, status
from . import models
from . import serializers
from rest_framework import filters
from django.db.models import Q
from modules.utilities.users_management import permissions as usersPermissions
from drf_spectacular.types import OpenApiTypes

#===================| Donkeys |===================#

@extend_schema(tags=["API - Sponsoring"],
               parameters=[
                   OpenApiParameter("local_id", OpenApiTypes.UUID, OpenApiParameter.QUERY)
               ])
class AnimalListCreate(generics.ListCreateAPIView):
    queryset = models.Animal.objects.all()
    serializer_class = serializers.AnimalSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        search_param = self.request.query_params.get('search', "")
        local_id = self.request.query_params.get('local_id', None)
        
        queryset = models.Animal.objects.all()
        if search_param:
            queryset = queryset.filter(
                Q(name__icontains=search_param) |
                Q(local_name__icontains=search_param)
            ).distinct()

        if local_id:
            queryset.filter(local_id=local_id)

        return queryset
    
class AnimalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Animal.objects.all()
    serializer_class = serializers.AnimalSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]

@extend_schema(tags=["API - Sponsoring"])
class SponsoredDonkeys(generics.ListAPIView):
    queryset = models.Animal.objects.all()
    serializer_class = serializers.AnimalSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request
        sponsoredIds = models.DonkeyOfSponsor.objects.filter(user=user).values_list('animal', flat=True)
        queryset = models.Animal.filter(id__in=sponsoredIds)
        return queryset
    
@extend_schema(tags=["API - Sponsoring"])
class NotMyDonkeys(generics.ListCreateAPIView):
    queryset = models.Animal.objects.all()
    serializer_class = serializers.AnimalSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [usersPermissions.IsDonkeyGodFather]

    def get_queryset(self):
        user = self.request.user
        print(user)
        sponsoredIds = models.DonkeyOfSponsor.objects.filter(user=user).values_list('animal', flat=True)
        return models.Animal.objects.exclude(id__in=sponsoredIds)
    
    def create(self, request, *args, **kwargs):
        donkeyId = request.data.get('donkey_id', None)
        value = request.data.get('value', 0)

        if not(donkeyId and value):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'bad request'})
        
        try:
            donkey = models.Animal.objects.get(id=donkeyId)
            sponsor = request.user
            stored, created = models.DonkeyOfSponsor.objects.update_or_create(animal=donkey,
                                                                              user=sponsor,
                                                                              defaults={
                                                                                'value': value
                                                                            })
            
            return Response(status=status.HTTP_202_ACCEPTED, data={'ok': f'Sponsor for {donkey.name} registered!'})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': f'{e}'})
        
    
#=================| Donkey Business |=================#


@extend_schema(tags=["API - Sponsoring"],
               parameters=[
                   OpenApiParameter("local_id", OpenApiTypes.UUID, OpenApiParameter.QUERY),
               ])
class AllActivities(generics.ListAPIView):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        queryset = models.Activity.objects.all()
        search_param = self.request.query_params.get('search', "")
        local_id = self.request.query_params.get('local_id', None)

        if search_param:
            queryset = queryset.filter(
                Q(title__icontains=search_param)
            )

        if local_id:
            local_donkeys = models.Animal.objects.filter(local_id=local_id)
            queryset = models.AnimalActivity.objects.filter(animal__in=local_donkeys).values('activity')
        
        return queryset

# Global view of my donkeys activities
@extend_schema(tags=["API - Sponsoring"])
class SponsoredDonkeys(generics.ListAPIView):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        sponsoredIds = models.DonkeyOfSponsor.objects.filter(user=user).values_list('animal', flat=True)
        activitiesIds = models.AnimalActivity.objects.filter(animal__in=sponsoredIds).values_list('activity', flat=True)
        queryset = models.Activity.objects.filter(id__in=activitiesIds)
        return queryset