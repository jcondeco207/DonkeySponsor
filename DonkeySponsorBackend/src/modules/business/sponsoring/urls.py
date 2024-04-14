from django.urls import path, include
from graphene_django.views import GraphQLView
from knox import views as knox_views
from modules.utilities.core.views import LoginView
from . import views

urlpatterns = [
    path('animals/', views.AnimalListCreate.as_view()),
    path('animals/new', views.NotMyDonkeys.as_view()),
    path('animals/sponsored', views.SponsoredDonkeys.as_view()),
]
