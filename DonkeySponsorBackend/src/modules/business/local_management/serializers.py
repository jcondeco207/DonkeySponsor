from rest_framework import serializers
from . import models
from modules.business.sponsoring import models as SponsorModels

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Local
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        donkeyCount = SponsorModels.Animal.objects.filter(local=instance).count()
        representation['donkey_count'] = donkeyCount
        return representation