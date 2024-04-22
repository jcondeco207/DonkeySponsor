import json

from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from knox.auth import TokenAuthentication
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from . import utils
from . import models
from . import serializers
from rest_framework import filters
from modules.business.local_management.models import Local
from modules.business.local_management.serializers import LocalSerializer

@extend_schema(tags=["API - Auth"])
@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({'detail': 'Please provide username and password.'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'detail': 'Invalid credentials.'}, status=400)

    login(request, user)
    return JsonResponse({'detail': 'Successfully logged in.'})

@extend_schema(tags=["API - Auth"])
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)

    logout(request)
    return JsonResponse({'detail': 'Successfully logged out.'})

@extend_schema(tags=["API - Auth"])
@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'isAuthenticated': True})

@extend_schema(tags=["API - Auth"])
def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})
    
    if request.user.role.name=='DonkeyProvider':
        locals = Local.objects.filter(owner = request.user)
        locals_data = LocalSerializer(locals, many=True).data
        return JsonResponse({'username': request.user.username, 'locals': locals_data, 'role': request.user.role.name})
    return JsonResponse({'username': request.user.username, 'role': request.user.role.name})