from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Movie(models.Model):
    class Meta:
        db_table = 'tbl_movies'

    name = models.CharField(max_length=100)
    year = models.IntegerField()
    content = models.TextField()
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.year}'


class MovieRating(models.Model):
    """
    評価の平均値を保存するためのテーブル
    """
    class Meta:
        db_table = 'tbl_movie_averages'

    movie = models.OneToOneField(
        Movie, on_delete=models.CASCADE, related_name='rating')
    average_star = models.FloatField(default=0)


class Role(models.Model):
    class Meta:
        db_table = 'tbl_roles'
    
    name = models.CharField(max_length=100)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='roles')
    
    def __str__(self):
        return f'{self.movie} {self.name}'


class Staff(models.Model):
    class Meta:
        db_table = 'tbl_staffs'

    name = models.CharField(max_length=100)
    birthday = models.DateField(default=None)
    roles = models.ManyToManyField(Role, related_name='staffs')
    
    def __str__(self):
        return f'{self.name} ({self.birthday})'


class Comment(models.Model):
    class Meta:
        db_table = 'tbl_comments'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    star = models.IntegerField()
    comment = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # 自身に紐づく Movie のコメントの評価平均を算出
        relate_comments = Comment.objects.filter(movie=self.movie)
        average_star = relate_comments.aggregate(models.Avg('star'))['star__avg']

        MovieRating.objects.update_or_create(
            movie=self.movie,
            average_star=average_star
        )

    def __str__(self):
        return f'movie: {self.movie} (Scored by{self.user}) Star: {self.star} comments: {self.comment}'
