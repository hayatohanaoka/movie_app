from django.contrib import admin

from .models import Movie, Role, Staff

# Register your models here.
admin.site.register(Movie)
admin.site.register(Role)
admin.site.register(Staff)
