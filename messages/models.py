from django.db import models
from djangotoolbox.fields import ListField
from djangotoolbox.fields import DictField


class Message(models.Model):

    timestamp = models.DateField()
    level = models.IntegerField()
    source = models.CharField(max_length=50)
    message = models.CharField(max_length=255)

    filename = models.CharField(max_length=255)
    line_number = models.IntegerField()

    payload = DictField()
    session = DictField()

    def __str__(self):
        return self.timestamp