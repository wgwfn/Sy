from django.db import models

# Create your models here.
class User(models.Model):

    gender = models.CharField(max_length=1, blank=True, null=True)
    age = models.IntegerField(blank=True,null=True)
    work = models.IntegerField(blank=True,null=True)
    username = models.CharField(max_length=16,blank=True,null=True)
    nickname = models.CharField(max_length=16,blank=True,null=True)
    password = models.CharField(max_length=20,blank=True,null=True)

    class Meta:
        db_table = 'user'

