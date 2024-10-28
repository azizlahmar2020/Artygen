from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, related_name='events_participated', blank=True)

    def __str__(self):
        return self.title
