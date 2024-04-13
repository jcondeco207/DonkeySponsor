from rest_framework import serializers
from . import models

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Animal
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)