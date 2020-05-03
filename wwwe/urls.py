from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from account import views as account_views
from pages import views as pages_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('signup/', account_views.user_signup, name='user_signup'),
    path('login/', account_views.user_login, name='user_login'),
    path('logout/', account_views.logout, name='logout'),

    path('', pages_views.home, name='home'),
    path('create_recipe/', pages_views.create_recipe, name='create_recipe'),
    path('my_recipes/', pages_views.my_recipes, name='my_recipes'),
    path('notifications/', pages_views.notifications, name='notifications'),
    path('settings/', pages_views.settings, name='settings'),
    path('settings/password', pages_views.settings_password, name='settings_password'),
    path('settings/email', pages_views.settings_email, name='settings_email'),

    url(r'^confirm_email/(?P<email_hash>\w{0,200})/$', pages_views.confirm_email, name='confirm_email'),

    url(r'^ajax/validate_username/$', pages_views.validate_username, name='validate_username'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# url(r'^$', account_views.home, name='home'),