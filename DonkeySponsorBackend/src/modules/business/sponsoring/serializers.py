from rest_framework import serializers
from . import models

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Animal
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)
    
class AnimalImageSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.AnimalImage
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)
    
class AnimalActivity(serializers.ModelSerializer):
    class Meta:
        model = models.AnimalActivity
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)
    
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnimalActivity
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)
    
class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnimalActivity
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)
    
class DonkeyOfSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DonkeyOfSponsor
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)