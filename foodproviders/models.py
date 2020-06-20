from django.db import models
from account.models import Account
#from django.contrib.gis.db import models


class FoodProviders(models.Model):
    provider_name = models.CharField(max_length=200)
    provider_description = models.TextField(blank=True)
    provider_user = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)
    provider_address = models.CharField(max_length=300)
    provider_lat = models.FloatField(default=0.0)
    provider_long = models.FloatField(default=0.0)
    #geoCoords = models.PointField(null=True, blank=True)

    added_date = models.DateTimeField()

    def __str__(self):
        return self.provider_name


class FollowerProvider(models.Model):
    followerProvider = models.ForeignKey(Account, related_name='targetProvider', null=True,  on_delete=models.SET_NULL)
    targetProvider = models.ForeignKey(FoodProviders, related_name='followerProvider', null=True,  on_delete=models.SET_NULL)

    def __str__(self):
        return self.followerProvider.username + " -> " + self.targetProvider.provider_name