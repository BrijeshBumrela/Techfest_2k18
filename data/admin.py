from django.contrib import admin

from . import models

# Register your models here.

admin.site.register((models.Event,
                     models.EventCatalogue,
                     models.EventCatagory,
                     models.Committee,
                     models.CommitteeContactInfo,
                     models.Notification,
                     ))
