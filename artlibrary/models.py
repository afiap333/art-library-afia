from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    roles=(('patron','Patron'),('librarian','Librarian'),)
    user_role=models.CharField(max_length=12,choices=roles, default='patron')
    def librarian_check(self):
        return self.user_role=='librarian'
    def is_patron(self):
        return self.user_role=='patron'

class ArtSupply(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='art_supplies/')
    quantity = models.PositiveIntegerField()
    pickup_location = models.CharField(max_length=255)
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)