from django.urls import include , path
from .views import ProfileViewsets
from rest_framework import routers
Roter=routers.DefaultRouter()
Roter.register(r'Profile', ProfileViewsets)

urlpatterns = [
    path('',include(Roter.urls)),
]