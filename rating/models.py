from django.db import models

# Create your models here.
class Rating(models.Model):
    movies = models.ForeignKey('movie.Movie',blank=True,null=True,on_delete=models.CASCADE)
    user = models.ForeignKey('user.User',blank=True,null=True,on_delete=models.CASCADE)
    rating = models.FloatField(blank=True,null=True)
    datetime = models.DateField(blank=True,null=True)
    class Meta:
        db_table = 'rating'