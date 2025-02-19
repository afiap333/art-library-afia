from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Patron(models.Model):
    patron_name=models.CharField(max_length=200)
    patron_date_joined=models.DateTimeField("date joined")

class Librarian(models.Model):
    librarian_name=models.CharField(max_length=200)
    librarian_date_joined=models.DateTimeField("date joined")

class ArtSupply(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='art_supplies/')
    quantity = models.PositiveIntegerField()
    pickup_location = models.CharField(max_length=255)
    added_by = models.ForeignKey(Librarian, on_delete=models.CASCADE)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)