


from django.db import models
from django.contrib.auth.models import AbstractUser
# from phonenumber_field.modelfields import PhoneNumberField
# from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone

from django.conf import settings
from countries_states_cities.models import Country, State, City,Region
# https://pypi.org/project/django-countries-states-cities/ ---->this is countries-states-cities pakage link address


# from django_countries.fields import CountryField
# from cities_light.models import Country, Region, City




class Profile(models.Model):
    """
    user -->foreignKey to User model
    bio --> writing something
    
     
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True, unique=True)
    image=models.ImageField(blank=True,null=True)
    # country = CountryField()
    # state = StateField(country='country')  # Make state dependent on country
    # city = CityField(state='state')  # Make city dependent on state
    
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE, related_name='country')
    # state = State(country='country')
    # city = City(state='state')
    state = models.ForeignKey(State,blank=True, null=True, on_delete=models.CASCADE, related_name='state')
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.CASCADE, related_name='city')
    avatar = models.ImageField(blank=True, null=True)

    

# # this class for story
class Story(models.Model):
    """
        Story --> ForeignKey to the User model and every one can create or write many Story
        likes --> ManyToManyField to User for lik any Story
        image --> for pictuer
        video --> for uplode video
        created ---> date of created
        update ---> date of updated
    """
    story=models.ForeignKey(User,on_delete=models.CASCADE,related_name='story',blank=True,null=True)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='profile',blank=True,null=True)
    likes=models.ManyToManyField(User,related_name='story_likes',blank=True) 
    image=models.ImageField(blank=True,null=True)
    video=models.FileField(blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    
    def __str__(self):
        return self.story.username
    
    def number_of_lik_of_storymodel(self):
        """
        this functhion returend number of like
        """
        return self.likes.count()

# this class for history
class Post(models.Model):
    """
        post --> ForeignKey to the User model and every one can create many postt for his profile
        likes --> ManyToManyField to User for lik any comment
        profile_post --> ForeignKey to the User model
        text --> write comment
        image --> for pictuer
        video --> for uplode video
        created ---> date of created
    """
    post=models.ForeignKey(User,on_delete=models.CASCADE,related_name='post',blank=True,null=True)
    profile_post=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='profile_post',blank=True,null=True)
    likes=models.ManyToManyField(User,related_name='likes',blank=True) #,on_delete=models.DO_NOTHING
    image=models.ImageField(blank=True,null=True)
    video=models.FileField(blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    
    def number_of_lik_of_postmodel(self):
        """
        this functhion returend number of like
        """
        return self.likes.count()


# this class for comment to anywhere
class Comment(models.Model):
    """
        comment --> ForeignKey to the User model and every one can create or write many comment
        likes --> ManyToManyField to User for lik any comment
        text --> write comment
        created ---> date of created
        update ---> date of updated
    """
    comment=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment',blank=True,null=True)
    likes=models.ManyToManyField(User,related_name='comment_like',blank=True)
    text=models.TextField(blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update=models.DateTimeField(auto_now=True,blank=True,null=True)
    
    
    def number_of_lik_of_commentmodel(self):
        """
        this functhion returend number of like
        """
        return self.likes.count()



    