from django.urls import path, include
from graphene_django.views import GraphQLView
from knox import views as knox_views
from modules.utilities.core.views import LoginView
from . import views

urlpatterns = []
