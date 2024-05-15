from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Movie, Staff, Role
from .serializers import MovieSerializer, StaffSerializer, RoleSerializer, RoleDetailSerializer, StaffDetailSerializer

# Create your views here.
class MovieListCreate(generics.ListCreateAPIView):

    serializer_class = MovieSerializer

    def get_queryset(self):
        return Movie.objects.filter(is_accepted=True)

class MovieRetrieveView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'

class StaffRetrieveView(generics.RetrieveAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffDetailSerializer
    lookup_field = 'id'

class RoleRetrieveView(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleDetailSerializer
    lookup_field = 'id'

movie_list_create = MovieListCreate.as_view()
movie_retrieve_view = MovieRetrieveView.as_view()
staff_retrieve_view = StaffRetrieveView.as_view()
role_retrieve_view = RoleRetrieveView.as_view()
