from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    content = models.TextField()
    is_accepted = models.BooleanField(default=True)

    class Meta:
        db_table = 'tbl_movies'
