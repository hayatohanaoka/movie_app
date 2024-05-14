from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Movie
from .serializers import MovieSerializer

# Create your views here.
class MovieListCreate(generics.ListCreateAPIView):

    serializer_class = MovieSerializer

    def get_queryset(self):
        return Movie.objects.filter(is_accepted=True)#.prefetch_related('roles')

movie_list_create = MovieListCreate.as_view()
