from django.shortcuts import render
from rest_framework import viewsets
from .serializers import Profileserializers
from account.models import *

# Create your views here.
class ProfileViewsets(viewsets.ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class=Profileserializers