from django.urls import path

from . import views

urlpatterns = [
    path('movies/', views.movie_list_create, name='movie_list_create'),
]
