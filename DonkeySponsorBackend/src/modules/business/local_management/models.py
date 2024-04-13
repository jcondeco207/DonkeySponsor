from django.db import models
import uuid
from Donkey_Sponsor.settings import AUTH_USER_MODEL


class Local(models.Model):
    id = models.UUIDField( primary_key=True,
                            unique=True,
                            default=uuid.uuid4,
                            editable=False)
    
    latitude = models.CharField()
    longitude = models.CharField()
    name = models.CharField()
    description = models.TextField()
    owner = models.ForeignKey(AUTH_USER_MODEL,
                              related_name='local',
                              on_delete=models.CASCADE)