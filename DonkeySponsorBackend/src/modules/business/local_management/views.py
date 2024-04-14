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


# -> Listar locais
# -> Listar burros de um local 
# -> Criar/Associar burros (donkey provider do local)
# -> publicar atividades dos burros
# -> Contar quantos padrinhos tem um burro