from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from account import views as account_views
from pages import views as pages_views
from recipe import views as recipe_views
from api import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('signup/', account_views.user_signup, name='user_signup'),
    path('login/', account_views.user_login, name='user_login'),
    path('logout/', account_views.logout, name='logout'),

    path('', pages_views.home, name='home'),
    path('create_recipe/', pages_views.create_recipe, name='create_recipe'),
    path('my_recipes/', pages_views.my_recipes, name='my_recipes'),
    path('my_followers/', pages_views.my_followers, name='my_followers'),
    path('my_followings/', pages_views.my_followings, name='my_followings'),
    path('notifications/', pages_views.notifications, name='notifications'),
    path('settings/', pages_views.settings, name='settings'),
    path('settings/password', pages_views.settings_password, name='settings_password'),
    path('settings/email', pages_views.settings_email, name='settings_email'),



    url(r'^cuisine/(?P<cuisine_id>\w{0,50})/$', pages_views.cuisine, name='cuisine'),
    url(r'^category/(?P<category_id>\w{0,50})/$', pages_views.category, name='category'),
    url(r'^tag/(?P<tag_id>\w{0,50})/$', pages_views.tag, name='tag'),
    url(r'^user/(?P<user_name>\w{0,50})/$', account_views.userPage, name='userPage'),



    url(r'^recipe/(?P<recipe_id>\w{0,50})/$', recipe_views.recipe, name='recipe'),

    url(r'^confirm_email/(?P<email_hash>\w{0,200})/$', pages_views.confirm_email, name='confirm_email'),

    url(r'^ajax/validate_username/$', pages_views.validate_username, name='validate_username'),
    url(r'^ajax/create_recipe_ajax/', pages_views.create_recipe_ajax, name='create_recipe_ajax'),
    url(r'^ajax/change_avatar/', pages_views.change_avatar, name='change_avatar'),

    path('api/', include('api.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# url(r'^$', account_views.home, name='home'),