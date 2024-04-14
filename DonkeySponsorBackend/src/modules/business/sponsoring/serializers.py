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
        animal_images_data = validated_data.pop('animal_image')
        animal = models.Animal.objects.create(**validated_data)
        for animal_image_data in animal_images_data:
            models.AnimalImage.objects.create(animal=animal, **animal_image_data)
        return animal
    
class AnimalActivity(serializers.ModelSerializer):
    class Meta:
        model = models.AnimalActivity
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)
    
class ActivitySerializer(serializers.ModelSerializer):
    activity_image = AnimalImageSerializer(many=True, required=False)

    class Meta:
        model = models.AnimalActivity
        fields = '__all__'

    class Meta:
        model = models.Animal
        fields = ['id', 'description', 'status', 'lastUpdatedAt', 'createdAt', 'activity_image']

    def create(self, validated_data):
        activity_images_data = validated_data.pop('activity_image')
        activity = models.Activity.objects.create(**validated_data)
        for activity_image_data in activity_images_data:
            models.ActivityImage.objects.create(activity=activity, **activity_image_data)
        return activity
    
class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActivityImage
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)
    
class DonkeyOfSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DonkeyOfSponsor
        fields = '__all__'