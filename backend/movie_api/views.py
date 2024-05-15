from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib import auth

from .models import Movie, Staff, Role
from .serializers import (
    MovieSerializer,
    RoleDetailSerializer,
    StaffDetailSerializer,
    UserRegistSerializer,
    UserLoginSerializer,
)


# Create your views here.
class UserRegistView(generics.CreateAPIView):
    serializer_class = UserRegistSerializer
    permission_classes = (permissions.AllowAny,)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, req):
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            user = auth.authenticate(
                request=req,
                username=req.data['username'],
                password=req.data['password']
            )
            
            if not user:
                return Response('認証失敗', status=status.HTTP_401_UNAUTHORIZED)
            
            auth.login(req, user)
            return Response('ログイン完了', status=status.HTTP_202_ACCEPTED)
        return Response('リクエストが不正です', status=status.HTTP_400_BAD_REQUEST)


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
user_regist_view = UserRegistView.as_view()
user_login_view = UserLoginView.as_view()
