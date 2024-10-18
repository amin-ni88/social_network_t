

from django.urls import path
from .views import *


urlpatterns = [
    path('', login_attempt, name="login"),
    path('register/', register, name="register"),
    path('otp/', otp, name="otp"),
    path('logoutt/', CustomLogoutView.as_view(), name='logout'),
    path('password_reset/', password_reset_request, name="password_reset"),
    path('reset/<uid>/<token>/', confirm_temp_password, name="confirm_temp_password"),
    path('email_login/', email_login, name="email_login"),
]


    




   

