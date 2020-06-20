from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from account import views as account_views

from recipe import views as recipe_views
from foodproviders import views as foodprovider_views


urlpatterns = [
    path('admin/', admin.site.urls),



    path('signup/', account_views.user_signup, name='user_signup'),
    path('login/', account_views.user_login, name='user_login'),
    path('logout/', account_views.logout, name='logout'),



    path('become_fp/', foodprovider_views.become_fp, name='become_fp'),
    url(r'^provider/(?P<provider_id>\w{0,50})/$', foodprovider_views.providerPage, name='providerPage'),
    url(r'^provider-settings/(?P<provider_id>\w{0,50})/$', foodprovider_views.providerSettings, name='providerSettings'),
    url(r'^provider/(?P<provider_id>\w{0,50})/menus/$', foodprovider_views.providerMenus, name='providerMenus'),
    url(r'^provider/(?P<provider_id>\w{0,50})/followers/$', foodprovider_views.providerFollowers, name='providerFollowers'),



    url(r'^user/(?P<user_name>\w{0,50})/$', account_views.userPage, name='userPage'),
    url(r'^user/(?P<user_name>\w{0,50})/followers/$', account_views.userFollowers, name='userFollowers'),
    url(r'^user/(?P<user_name>\w{0,50})/providers/$', account_views.userProviders, name='userProviders'),


    url(r'^recipe/(?P<recipe_id>\w{0,50})/$', recipe_views.recipe, name='recipe'),


    url(r'^', include('pages.urls')),
    path('api/', include('api.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# url(r'^$', account_views.home, name='home'),