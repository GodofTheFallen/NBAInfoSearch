from django.db import models


# Create your models here.


class KeyWord(models.Model):
    id = models.IntegerField(primary_key=True)
    word = models.TextField()
    idf = models.FloatField()


class NewsPage(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField()
    title = models.TextField()
    time = models.DateTimeField()
    source_name = models.TextField()
    source_url = models.URLField()
    body = models.TextField()
    keywords = models.ManyToManyField(KeyWord)
    title_key_mod = models.FloatField(default=0.0)
    body_key_mod = models.FloatField(default=0.0)

    def get_absolute_url(self):
        return '/newspage/' + str(self.id)
