from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    # image field add korlam
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    rsvped_users = models.ManyToManyField(User, related_name='rsvped_events', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

