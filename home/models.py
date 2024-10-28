# home/models.py

from django.db import models

class Artwork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
