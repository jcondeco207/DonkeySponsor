from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import render
from django.conf.urls.static import static

# API Documentation
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


# Permissions
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from Donkey_Sponsor import settings
# OTP
from two_factor.urls import urlpatterns as tf_urls
from axes.decorators import axes_dispatch
from django.urls import URLPattern
from rest_framework import permissions

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

def favicon(request):
    return render(request, 'dist/index.html')
 
# Apply Axes control check to Django-Two-Factor-Auth methods
for pattern in tf_urls[0]:
    if type(pattern) != URLPattern:
         continue
    
    if pattern.callback:
      pattern.callback = axes_dispatch(pattern.callback)

admin.site.site_title = "Donkey Sponsor - Admin"
admin.site.site_header = "Donkey Sponsor - Admin"
admin.site.index_title = "Cloud Computing - 2023/2024"

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Two factor auth and sessions urls
    path('', include(tf_urls)),
    path('', include('user_sessions.urls', 'user_sessions')),
    path("accounts/", include("django.contrib.auth.urls")),
    re_path(r'^favicon\.ico$', favicon, name='favicon'),

    # Documentation
    path('docs/download', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API
    path('api/', include('modules.api.urls')),
    path('api/', include('modules.business.local_management.urls')),
    path('api/', include('modules.business.sponsoring.urls')),
    path('api/', include('modules.utilities.users_management.urls')),

    # React
    re_path(r'.*', index_view, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
