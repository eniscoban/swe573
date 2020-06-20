from django.urls import path
from . import views as pages_views
from django.conf.urls import url, include

urlpatterns = [
    path('', pages_views.home, name='home'),
    path('create_recipe/', pages_views.create_recipe, name='create_recipe_page'),
    path('my_recipes/', pages_views.my_recipes, name='my_recipes'),
    path('my_followers/', pages_views.my_followers, name='my_followers'),
    path('my_followings/', pages_views.my_followings, name='my_followings'),
    path('my_following_providers/', pages_views.my_following_providers, name='my_following_providers'),
    path('notifications/', pages_views.notifications, name='notifications'),
    path('settings/', pages_views.settings, name='settings'),
    path('settings/password', pages_views.settings_password, name='settings_password'),
    path('settings/email', pages_views.settings_email, name='settings_email'),
    path('search/', pages_views.search, name='search'),
    path('providers_near_me/', pages_views.providers_near_me, name='providers_near_me'),

    url(r'^cuisine/(?P<cuisine_id>\w{0,50})/$', pages_views.cuisine, name='cuisine'),
    url(r'^category/(?P<category_id>\w{0,50})/$', pages_views.category, name='category'),
    url(r'^tag/(?P<tag_id>\w{0,50})/$', pages_views.tag, name='tag'),

    url(r'^confirm_email/(?P<email_hash>\w{0,200})/$', pages_views.confirm_email, name='confirm_email'),

    url(r'^ajax/validate_username/$', pages_views.validate_username, name='validate_username'),
    url(r'^ajax/create_recipe_ajax/', pages_views.create_recipe_ajax, name='create_recipe_ajax'),

]
