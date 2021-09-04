from django.db import models

# Create your models here.
class RecommendMatrix(models.Model):
    id1 = models.IntegerField(blank=True,null=True)
    id2 = models.IntegerField(blank=True,null=True)
    factor = models.TextField(blank=True,null=True)
    class Meta:
        db_table = 'matrix'