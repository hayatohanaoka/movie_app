from rest_framework import serializers

from .models import Movie, Role, Staff

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
