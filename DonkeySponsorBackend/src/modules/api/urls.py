from django.urls import path, include
from graphene_django.views import GraphQLView
from knox import views as knox_views
from modules.utilities.core.views import LoginView
from . import views

urlpatterns = [
    # API Auth Logic
    path('token/', LoginView.as_view()),
    path('token/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('token/logout/all', knox_views.LogoutAllView.as_view(), name='knox_logout_all'),

    # Apps

    # Paths consumed by react session
    path('login/', views.login_view, name='api-login'),
    path('logout/', views.logout_view, name='api-logout'),
    path('session/', views.session_view, name='api-session'),
    path('whoami/', views.whoami_view, name='api-whoami')
]
