from django.urls import path
from . import views

urlpatterns = [
    path('list_all_recipes/', views.list_all_recipes, name='list_all_recipes'),
    path('list_my_recipes/', views.list_my_recipes, name='list_my_recipes'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('like_recipe/', views.like_recipe, name='like_recipe'),
    path('unlike_recipe/', views.unlike_recipe, name='unlike_recipe'),

    path('follow_user/', views.follow_user, name='follow_user'),
    path('unfollow_user/', views.unfollow_user, name='unfollow_user'),

    path('create_foodprovider/', views.create_foodprovider, name='create_foodprovider'),
    path('edit_foodprovider/', views.edit_foodprovider, name='edit_foodprovider'),

    path('getTagsFromWikidata/', views.getTagsFromWikidata, name='getTagsFromWikidata'),

    path('createMenu/', views.createMenu, name='createMenu'),
    path('addToMenu/', views.addToMenu, name='addToMenu'),
    path('removeFromMenu/', views.removeFromMenu, name='removeFromMenu'),

    path('follow_provider/', views.follow_provider, name='follow_provider'),
    path('unfollow_provider/', views.unfollow_provider, name='unfollow_provider'),


    path('change_avatar/', views.change_avatar, name='change_avatar'),




    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
