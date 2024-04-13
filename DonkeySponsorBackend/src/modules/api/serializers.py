from rest_framework import serializers
from . import models
class APIResultSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    mensagem = serializers.CharField()
    resultado = serializers.ListField(child=serializers.JSONField())