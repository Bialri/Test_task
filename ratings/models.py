from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Comic(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    rating = models.FloatField(default=0,
                               validators=[MaxValueValidator(5), MinValueValidator(0)])

    def update_rating(self):
        user_ratings = Rating.objects.filter(comic_id=self.id).distinct('user_id')
        if user_ratings:
            ratings_count = len(user_ratings)
            rating_sum = sum([rating.VALUE for rating in user_ratings])
            rating = sum([rating.VALUE for rating in user_ratings]) / ratings_count
            self.rating = rating
            self.save()


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    comic_id = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='ratings')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    VALUE = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)])
