from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User_Data(AbstractUser):
    favourite_place = models.CharField(max_length=30, null=True,blank=True)



