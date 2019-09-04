from django.db import models


# Create your models here.

class NewsPage(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField()
    title = models.TextField()
    time = models.DateTimeField()
    source_name = models.TextField()
    source_url = models.URLField()
    body = models.TextField()
