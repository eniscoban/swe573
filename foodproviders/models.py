from django.db import models
from account.models import Account

class FoodProviders(models.Model):
    provider_name = models.CharField(max_length=200)
    provider_description = models.TextField(blank=True)
    provider_user = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)
    provider_address = models.CharField(max_length=300)
    provider_lat = models.FloatField(default=0.0)
    provider_long = models.FloatField(default=0.0)

    added_date = models.DateTimeField()

    def __str__(self):
        return self.provider_name
