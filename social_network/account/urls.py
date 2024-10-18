from . views import *
from django.urls import path,include
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('' , login_attempt , name="login"),
    path('register' , register , name="register"),
    path('otp' , otp , name="otp"),
    path('logoutt/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('reset', reset_password , name='reset_password'),
    path('accounts/reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]
