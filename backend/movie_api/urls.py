from django.urls import path

from . import views

urlpatterns = [
    path('regist/', views.user_regist_view, name='user_regist_view'),
    path('login/', views.user_login_view, name='user_login_view'),
    path('movies/', views.movie_list_create, name='movie_list_create'),
    path('movies/<int:id>/', views.movie_retrieve_view, name='movie_retrieve_view'),
    path('movies/<int:id>/comments/', views.comment_list_view, name='comment_list_view'),
    path('movies/<int:id>/comments/<int:cmt_id>/',
        views.comment_retrieve_view, name='comment_retrieve_view'),
    path('roles/<int:id>/', views.role_retrieve_view, name='role_retrieve_view'),
    path('staffs/<int:id>/', views.staff_retrieve_view, name='staff_retrieve_view'),
]
