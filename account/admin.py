from django.contrib import admin
from account.models import Account,Follower, Allergies, UserAllergies

admin.site.register(Account)
admin.site.register(Follower)
admin.site.register(Allergies)
admin.site.register(UserAllergies)