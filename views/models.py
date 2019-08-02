import datetime, os

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone

file_storage = FileSystemStorage()

class Image(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    image = models.FileField(storage=file_storage)
    pub_date = models.DateTimeField('date published')

    @property
    def filename(self):
        return os.path.basename(self.image.name)

class Keyword(models.Model):
    keyword = models.CharField(max_length=200)
    uses = models.IntegerField(default=0)

    def __str__(self):
        return self.keyword