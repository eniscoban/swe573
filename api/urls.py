from django.urls import path
from . import views

urlpatterns = [
    path('list_all_recipes/', views.list_all_recipes, name='list_all_recipes'),
    path('list_my_recipes/', views.list_my_recipes, name='list_my_recipes'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),


    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
