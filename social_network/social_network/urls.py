"""
URL configuration for social_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from account import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', views.login_attempt, name='login_attempt'),  # Unique path for login attempt
    path('register/', views.register, name='register'),
    path('otp/', views.otp, name='otp'),  
    path('sendemail', views.send_email, name='email'),
    path('login/', views.CustomLogoutView.as_view(), name='login'),  # Correct usage  # Ensure this is correctly set up
    path('accounts/', include('account.urls')),  # Include accounts URLs
    path('reset', views.reset_password , name='reset_password'),
    path('accounts/reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('home/', include('cart.urls')),
    path('API', include('API.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

