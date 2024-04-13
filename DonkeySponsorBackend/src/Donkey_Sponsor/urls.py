from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# API Documentation
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Permissions
from rest_framework import permissions
from django.contrib.auth.decorators import login_required

# OTP
from two_factor.urls import urlpatterns as tf_urls

# GraphQL
from graphene_django.views import GraphQLView

schema_view = get_schema_view(
   openapi.Info(
      title="Django Bridge",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# React
def index_view(request):
    return render(request, 'dist/index.html')

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Two factor auth and sessions urls
    path('', include(tf_urls)),
    path('', include('user_sessions.urls', 'user_sessions')),

    # Documentation
    path('docs/download', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API
    path('api/', include('modules.api.urls')),

    # React
    path('', login_required(index_view), name='index'),
]