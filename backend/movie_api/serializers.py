from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Movie, Role, Staff, Comment

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('name', 'birthday', 'roles')


class RoleSerializer(serializers.ModelSerializer):
    staffs = StaffSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'year', 'content', 'roles')


class RoleDetailSerializer(serializers.ModelSerializer):
    # dict のような形式で出力する
    # staffs = StaffSerializer(many=True, read_only=True)
    # movie = MovieSerializer(read_only=True)

    # Models の __str__で定義した形式で出力する
    staffs = serializers.StringRelatedField(many=True, read_only=True)
    movie = serializers.StringRelatedField()  # 変数名に設定したモデルと紐づく？

    class Meta:
        model = Role
        fields = ('name', 'staffs', 'movie')


class StaffDetailSerializer(serializers.ModelSerializer):
    # dict のような形式で出力する
    # roles = RoleDetailSerializer(many=True)

    # Models の __str__で定義した形式で出力する
    roles = serializers.StringRelatedField(many=True)

    class Meta:
        model = Staff
        fields = ('name', 'birthday', 'roles')


class UserRegistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        data_keys = data.keys()
        if 'username' not in data_keys or 'password' not in data_keys:
            raise serializers.ValidationError('username と password は必須項目です')
        return data


class CommentSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField(many=False, read_only=True)
    user = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'star', 'comment', 'movie', 'user')
    
    def validate_star(self, val):
        if val < 0 or val > 5:
            raise serializers.ValidationError('0 ~ 5 で評価してください')
        return val

    def check_comment_exists(self, user, movie_id):
        if Comment.objects.filter(user=user, movie_id=movie_id).exists():
            raise serializers.ValidationError('既に評価・コメント済みです')
