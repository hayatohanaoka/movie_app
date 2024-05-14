from rest_framework import serializers

from .models import Movie, Role, Staff

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    staffs = StaffSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):

    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'year', 'content', 'roles',)

