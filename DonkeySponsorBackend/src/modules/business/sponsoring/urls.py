from django.urls import path, include
from graphene_django.views import GraphQLView
from knox import views as knox_views
from modules.utilities.core.views import LoginView
from . import views

urlpatterns = [
    path('animals/', views.AnimalListCreate.as_view()),
    path('animals/<uuid:pk>', views.AnimalDetail.as_view()),
    path('animals/<uuid:donkey_id>/remove_sponsor', views.RemoveSponsor.as_view()),
    path('animals/new', views.NotMyDonkeys.as_view()),
    path('animals/sponsored', views.SponsoredDonkeysList.as_view()),
    path('activities/', views.AllActivities.as_view()),
    path('activities/sponsored', views.SponsoredDonkeys.as_view())
]
