from django.db import models


class Message(models.Model):

    timestamp = models.DateField()
    level = models.IntegerField()
    source = models.CharField(max_length=50)
    message = models.CharField(max_length=255)

    filename = models.CharField(max_length=255)
    line_number = models.IntegerField()

    payload = models.TextField()
    session = models.TextField()

    def __str__(self):
        return self.timestamp