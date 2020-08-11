from django.contrib import admin
from first_api import models

# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Article)
admin.site.register(models.ProfileFeedItem)

# Home Secure main registers

admin.site.register(models.Company)
admin.site.register(models.Village)
admin.site.register(models.Zone)
