from django.db import models
import uuid



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
    