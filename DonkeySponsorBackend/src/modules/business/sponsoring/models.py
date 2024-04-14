from django.db import models
import uuid
from Donkey_Sponsor.settings import AUTH_USER_MODEL

class Animal(models.Model):
    id = models.UUIDField( primary_key=True,
                            unique=True,
                            default=uuid.uuid4,
                            editable=False)
    name = models.CharField()
    color = models.CharField()
    status = models.BooleanField()
    
    local = models.ForeignKey('local_management.Local',
                                related_name='animal',
                                on_delete=models.CASCADE)
    
class AnimalImage(models.Model):
    id = models.UUIDField( primary_key=True,
                            unique=True,
                            default=uuid.uuid4,
                            editable=False)
    
    animal = models.ForeignKey('sponsoring.Animal',
                                related_name='animal_image',
                                on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='uploads/',
                              null=True)

class AnimalActivity(models.Model):
    id = models.UUIDField( primary_key=True,
                           unique=True,
                           default=uuid.uuid4,
                           editable=False)
    
    animal = models.ForeignKey('sponsoring.Animal',
                                related_name='animal_activity',
                                on_delete=models.CASCADE)
    
    activity = models.ForeignKey('Activity',
                                related_name='activity',
                                on_delete=models.CASCADE)
    
class Activity(models.Model):
    id = models.UUIDField( primary_key=True,
                           unique=True,
                           default=uuid.uuid4,
                           editable=False) 
    
    description = models.CharField()
    status = models.BooleanField()
    lastUpdatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now=True)

class ActivityImage(models.Model):
    id = models.UUIDField( primary_key=True,
                           unique=True,
                           default=uuid.uuid4,
                           editable=False) 
    
    activity = models.ForeignKey('sponsoring.Activity',
                            related_name='activity_image',
                            on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='uploads/',
                              null=True)
    
class DonkeyOfSponsor(models.Model):
    id = models.UUIDField( primary_key=True,
                           unique=True,
                           default=uuid.uuid4,
                           editable=False) 
    
    user = models.ForeignKey(AUTH_USER_MODEL,
                              related_name='donkey_of_sponsor',
                              on_delete=models.CASCADE)
    
    animal = models.ForeignKey('sponsoring.Animal',
                               related_name='donkey_of_sponsor',
                               on_delete=models.CASCADE)

    value = models.FloatField()
    
    createdAt = models.DateTimeField(auto_now=True)

    status = models.BooleanField()