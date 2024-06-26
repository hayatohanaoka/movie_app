"""
generic api viewで作成したAPIを書き換えたものを入れる
"""

from django.shortcuts import render, redirect
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Movie
from .serializers import MovieSerializer, UserRegistSerializer

# Create your views here.
class MovieListCreate(APIView):

    serializer_class = MovieSerializer
    model = Movie

    def get(self, req):
        items = self.model.objects.filter(is_accepted=True)
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)
    
    def post(self, req):
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect(to='api/')
        return Response('不正なリクエストでした', status=status.HTTP_400_BAD_REQUEST)


class UserRegistView(APIView):
    serializer_class = UserRegistSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, req):
        return Response('登録画面', status=status.HTTP_200_OK)
    
    def post(self, req):
        serializer = UserRegistSerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('登録完了', status=status.HTTP_201_CREATED)
        return Response('登録失敗', status=status.HTTP_400_BAD_REQUEST)

movie_list_create = MovieListCreate.as_view()
