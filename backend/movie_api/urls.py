from django.urls import path

from . import views

urlpatterns = [
    path('regist/', views.user_regist_view, name='user_regist_view'),
    path('movies/', views.movie_list_create, name='movie_list_create'),
    path('movies/<int:id>/', views.movie_retrieve_view, name='movie_retrieve_view'),
    path('roles/<int:id>/', views.role_retrieve_view, name='role_retrieve_view'),
    path('staffs/<int:id>/', views.staff_retrieve_view, name='staff_retrieve_view'),
]
