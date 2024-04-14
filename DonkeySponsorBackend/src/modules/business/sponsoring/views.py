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

#===================| Donkeys |===================#

@extend_schema(tags=["API - Sponsoring"])
class AnimalListCreate(generics.ListCreateAPIView):
    queryset = models.Animal.objects.all()
    serializer_class = serializers.AnimalSerializer
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        search_param = self.request.query_params.get('search', "")
        if search_param:
            queryset = queryset.filter(
                Q(name__icontains=search_param) |
                Q(local_name__icontains=search_param)
            )
        return queryset
    
class AnimalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Animal.objects.all()
    serializer_class = serializers.AnimalSerializer

@extend_schema(tags=["API - Sponsoring"])
class SponsoredDonkeys(generics.ListAPIView):
    queryset = models.Animal.objects.all()
    serializer_class = serializers.AnimalSerializer

    def get_queryset(self):
        user = self.request
        sponsoredIds = models.DonkeyOfSponsor.objects.filter(user=user).values_list('animal', flat=True)
        queryset = models.Animal.filter(id__in=sponsoredIds)
        return queryset
    
@extend_schema(tags=["API - Sponsoring"])
class NotMyDonkeys(generics.ListCreateAPIView):
    queryset = models.Animal.objects.all()
    serializer_class = serializers.AnimalSerializer

    def get_queryset(self):
        user = self.request
        sponsoredIds = models.DonkeyOfSponsor.objects.filter(user=user).values_list('animal', flat=True)
        return models.Animal.exclude(id__in=sponsoredIds)
    
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


@extend_schema(tags=["API - Sponsoring"])
class AllActivities(generics.ListAPIView):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer

# Global view of my donkeys activities
@extend_schema(tags=["API - Sponsoring"])
class SponsoredDonkeys(generics.ListAPIView):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer

    def get_queryset(self):
        user = self.request
        sponsoredIds = models.DonkeyOfSponsor.objects.filter(user=user).values_list('animal', flat=True)
        activitiesIds = models.AnimalActivity.filter(animal__in=sponsoredIds).values_list('activity', flat=True)
        queryset = models.Activity.filter(id__in=activitiesIds)
        return queryset