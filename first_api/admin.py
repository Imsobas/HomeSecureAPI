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
admin.site.register(models.Work)
admin.site.register(models.CustomFCMDevice)
admin.site.register(models.Manager)
admin.site.register(models.SecureWork)
admin.site.register(models.CheckinCheckpoint)
admin.site.register(models.Setting)
admin.site.register(models.PointObservation)
admin.site.register(models.PointObservationPointList)
admin.site.register(models.PointObservationRecord)
admin.site.register(models.MaintenanceFeePeriod)
admin.site.register(models.MaintenanceFeeRecord)
admin.site.register(models.VoteTopic)
admin.site.register(models.VoteCount)
admin.site.register(models.VoteChoice)
admin.site.register(models.VoteRecord)
admin.site.register(models.Problem)
admin.site.register(models.WorkingRecord)
admin.site.register(models.Notification)



