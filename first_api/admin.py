from django.contrib import admin
from first_api import models

# Register your models here.

admin.site.register(models.UserProfile)
# admin.site.register(models.Article)
# admin.site.register(models.ProfileFeedItem)

# Home Secure main registers

admin.site.register(models.Company)
admin.site.register(models.Village)
admin.site.register(models.Zone)
admin.site.register(models.Home)
admin.site.register(models.GeneralUser)
admin.site.register(models.SecureGuard)
admin.site.register(models.Qrcode)
admin.site.register(models.Checkpoint)

