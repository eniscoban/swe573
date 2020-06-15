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


    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
