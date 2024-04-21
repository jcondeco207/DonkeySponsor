from rest_framework import serializers
from . import models

class AnimalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnimalImage
        fields = ['id', 'image']

class AnimalSerializer(serializers.ModelSerializer):
    animal_image = AnimalImageSerializer(many=True, required=False)

    class Meta:
        model = models.Animal
        fields = ['id', 'name', 'color', 'status', 'local', 'animal_image']

    def create(self, validated_data):
        try:
            animal_images_data = validated_data.pop('animal_image')
        except:
            animal_images_data = []
            
        animal = models.Animal.objects.create(**validated_data)
        for animal_image_data in animal_images_data:
            models.AnimalImage.objects.create(animal=animal, **animal_image_data)
        return animal
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        sponsorCount = models.DonkeyOfSponsor.objects.filter(animal=instance).count()
        representation['sponsor_count'] = sponsorCount
        return representation
    
class AnimalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnimalActivity
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)

class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActivityImage
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)

class ActivitySerializer(serializers.ModelSerializer):
    activity_image = ActivityImageSerializer(many=True, required=False)
    donkey_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = models.Activity
        fields = ['id', 'title', 'description', 'status', 'lastUpdatedAt', 'createdAt', 'activity_image', 'donkey_id']


    def create(self, validated_data):
        activity_images_data = validated_data.pop('activity_image')
        donkey_id = validated_data.pop('donkey_id')
        activity = models.Activity.objects.create(**validated_data)
        animal_activity = models.AnimalActivity.objects.create(animal_id=donkey_id, activity=activity)
        for activity_image_data in activity_images_data:
            models.ActivityImage.objects.create(activity=activity, **activity_image_data)
        return activity
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['donkey_id'] = models.AnimalActivity.objects.filter(activity=instance).values_list('animal_id', flat=True)
        return representation
    
class DonkeyOfSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DonkeyOfSponsor
        fields = '__all__'


class FormmatedNewSponsor(serializers.Serializer):
    donkey_id = serializers.UUIDField()
    value = serializers.FloatField()