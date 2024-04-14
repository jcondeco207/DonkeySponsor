from django.contrib import admin
from . import models

admin.site.register(models.Animal)
admin.site.register(models.AnimalImage)
admin.site.register(models.AnimalActivity)
admin.site.register(models.Activity)
admin.site.register(models.ActivityImage)
admin.site.register(models.DonkeyOfSponsor)