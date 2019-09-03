from django.db import models


# Create your models here.

class NewsPage(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField()
    title = models.CharField(max_length=100)
    time = models.DateTimeField()
    source_name = models.CharField(max_length=20)
    source_url = models.URLField()
    body = models.CharField(max_length=5000)
