from django.db import models ####"To create tables for saving information in the database."
from django.contrib.auth.models import AbstractUser
#  "These imports are used to create a Custom User Model in Django."##


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,blank = True,null = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    

