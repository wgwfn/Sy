from django.db import models

# Create your models here.
class Movie(models.Model):

    title = models.TextField(blank=True,null=True)
    genres= models.TextField(blank=True,null=True)
    imbd = models.TextField(blank=True,null=True)
    url = models.ImageField(upload_to='imgs/',null=True)
    douban = models.TextField(blank=True,null=True)
    aditor = models.TextField(blank=True,null=True)
    actor = models.TextField(blank=True,null=True)
    releasedate = models.TextField(blank=True,null=True)
    runtime = models.TextField(blank=True,null=True)
    rename = models.TextField(blank=True,null=True)
    ares = models.TextField(blank=True,null=True)
    summary = models.TextField(blank=True,null=True)
    imdb_rating = models.FloatField(blank=True,null=True)
    douban_rating = models.FloatField(blank=True,null=True)

    class Meta:
        db_table = 'movie'

