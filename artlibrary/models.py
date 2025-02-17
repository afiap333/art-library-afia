from django.db import models

# Create your models here.

class Patrons(models.Models):
    patron_name=models.TextField(max_length=200)
    patron_date_joined=models.DateTimeField("date joined")
class Librarians(models.Models):
    librarian_name=models.TextField(max_length=200)
    librarian_date_joined=models.DateTimeField("date joined")
