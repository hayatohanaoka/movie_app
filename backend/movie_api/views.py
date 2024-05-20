from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.contrib import auth
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Comment, Movie, Staff, Role
from .serializers import (
    CommentSerializer,
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


class MovieListPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10


class MovieListCreate(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    pagination_class = MovieListPagination
    filter_backends  = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('name', 'roles__staffs__name', 'year')
    ordering_fields  = ('name', 'year')

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


class CommentListCreateView(generics.ListCreateAPIView):

    serializer_class = CommentSerializer

    def get_queryset(self):
        movie_id = self.kwargs['id']
        return Comment.objects.filter(movie_id=movie_id)
    
    def perform_create(self, serializer):
        user = self.request.user
        movie_id = self.kwargs['id']
        serializer.check_comment_exists(user, movie_id)
        serializer.save(
            user=user, movie_id=movie_id # 外部キーをセットする
        )


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'cmt_id'
    lookup_field = 'id'  # Comment のフィルター条件にするカラム

    def get_queryset(self):
        movie_id = self.kwargs['id']
        return Comment.objects.filter(movie_id=movie_id)


movie_list_create = MovieListCreate.as_view()
movie_retrieve_view = MovieRetrieveView.as_view()
staff_retrieve_view = StaffRetrieveView.as_view()
role_retrieve_view = RoleRetrieveView.as_view()
user_regist_view = UserRegistView.as_view()
user_login_view = UserLoginView.as_view()
comment_list_view = CommentListCreateView.as_view()
comment_retrieve_view = CommentRetrieveUpdateDestroyAPIView.as_view()
