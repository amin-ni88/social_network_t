from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    password= models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=20)
    otp = models.CharField(max_length=4)
    bio = models.TextField(blank=True, default='')
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True, default='')
    