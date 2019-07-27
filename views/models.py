import datetime, os

from django.db import models
from django.utils import timezone


class Image(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    image = models.FileField(upload_to='views/static/uploads/')
    pub_date = models.DateTimeField('date published')

    @property
    def filename(self):
        return 'uploads/'+os.path.basename(self.image.name)

class Keyword(models.Model):
    keyword = models.CharField(max_length=200)
    uses = models.IntegerField(default=0)

    def __str__(self):
        return self.keyword