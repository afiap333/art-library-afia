from django.db import models
from django.contrib.auth.models import AbstractUser
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.exceptions import ValidationError

# Create your models here.

class CustomUser(AbstractUser):
    profile_pic = models.ImageField(
        storage=S3Boto3Storage(),  
        upload_to='profile_pics/',  
        null=True,
        blank=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    roles = (('patron', 'Patron'), ('librarian', 'Librarian'), ('anonymous', 'Anonymous'))
    user_role = models.CharField(max_length=12, choices=roles, default='patron')
    email = models.EmailField(blank=True, max_length=254, verbose_name='email address')
    def librarian_check(self):
        return self.user_role == 'librarian'
    
    def is_patron(self):
        return self.user_role == 'patron'
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
class Collection(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField(blank=True,null=True)
    num_items=models.PositiveIntegerField(default=0)
    is_public=models.BooleanField(default=True)
    users=models.ManyToManyField(CustomUser,blank=True,related_name='collections')
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_collections',default=2)
    def __str__(self):
        return self.title
    def update_num_items(self):
        if(self.is_public):
            self.num_items = self.public_items.count() 
        else:
            self.num_items = self.private_items.count()  
        self.save()
    
class ArtSupply(models.Model):
    STATUS = [
        ('available', 'Available'), 
        ('checked_out', 'Checked Out'),
    ]
    USE_TYPE=[
        ('single','Single Use'),
        ('multi','Multi Use'),
    ]
    name = models.CharField(max_length=255)
    image = models.ImageField(
        storage=S3Boto3Storage(),  # Ensures upload to S3
        upload_to='art_supplies/',  # S3 bucket folder
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    pickup_location = models.CharField(max_length=255)
    use_policy=models.TextField(null=True,blank=True)
    item_type=models.CharField(max_length=7,choices=USE_TYPE,default='multi')
    description = models.TextField(null=True, blank=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='added_items')
    collection = models.ManyToManyField(Collection, related_name='items', blank=True)
    def __str__(self):
        return self.name

class Reviews(models.Model):
    item=models.ForeignKey(ArtSupply,on_delete=models.CASCADE,related_name='ratings')
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField()
    comment=models.TextField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)