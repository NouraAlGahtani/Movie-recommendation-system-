from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie1', views.movie1, name='movie1'),
    path('movie2', views.movie2, name='movie2'),
path('movie3', views.movie3, name='movie3'),
path('movie4', views.movie4, name='movie4'),
path('movie5', views.movie5, name='movie5'),
path('movie6', views.movie6, name='movie6'),
path('movie7', views.movie7, name='movie7'),
path('movie8', views.movie8, name='movie8'),


]