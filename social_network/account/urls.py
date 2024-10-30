from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
import random
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib import messages
from kavenegar import KavenegarAPI
import smtplib
from email.message import EmailMessage
import ssl
import string
import os
import logging

logger = logging.getLogger(__name__)

def send_otp(request, mobile):
    otp = random.randint(1000, 9999)
    api = KavenegarAPI(os.getenv('KAVENEGAR_API_KEY'))  # Use environment variable for API key
    params = {
        'sender': 'YourSender',  # Use a verified sender
        'receptor': mobile,
        'message': f'Your OTP is: {otp}'
    }

    profile = Profile.objects.filter(mobile=mobile).first()
    if profile:
        profile.otp = otp
        profile.save()

    try:
        response = api.sms_send(params)
        logger.info(response)
    except Exception as e:
        logger.error(f"Error sending OTP: {e}")

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

def otp(request):
    mobile = request.session.get('mobile')
    context = {'mobile': mobile}

    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()

        if profile and otp == str(profile.otp):
            return redirect('cart')
        else:
            context['message'] = 'Wrong OTP'
            context['class'] = 'danger'

    return render(request, 'otp.html', context)

def login_attempt(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)

        if user is not None:
            login(request, user)
            return redirect('cart')
        else:
            context = {'message': 'User does not exist or password is incorrect', 'class': 'danger'}
            return render(request, 'login.html', context)

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        # Check for existing user by email and profile by mobile
        if User.objects.filter(email=email).exists():
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'register.html', context)

        if Profile.objects.filter(mobile=mobile).exists():
            context = {'message': 'Mobile number already registered', 'class': 'danger'}
            return render(request, 'register.html', context)

        # Create a new user
        user = User(email=email, first_name=name)
        user.set_password(password)  # Set the password securely
        user.save()  # Save the user to the database

        # Create a profile for the user
        otp = str(random.randint(1000, 9999))
        profile = Profile(user=user, mobile=mobile, otp=otp)
        profile.save()  # Save the profile to the database

        # Send OTP
        send_otp(request, mobile)

        # Store mobile in session
        request.session['mobile'] = mobile

        # Log in the user
        login(request, user)

        # Redirect to the cart
        return redirect('cart')

    return render(request, 'register.html')


def send_email(email_reciver, password):
    email_sender = os.getenv('ghazalfarokh51@gmail.com')  # Use environment variable for sender email
    email_password = os.getenv('EMAIL_PASSWORD')  # Use environment variable for sender email password
    subject = "Password Reset"
    body = f"Your password: {password}"
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciver, em.as_string())

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        profile = Profile.objects.filter(email=email).first()
        if profile:  # Check if the profile exists
            length = random.randint(8, 20)
            characters = string.ascii_letters + string.digits
            new_password = ''.join(random.choice(characters) for _ in range(length))
            send_email(email, new_password)

            # Update the user's password
            user = profile.user
            user.set_password(new_password)
            user.save()

            messages.success(request, 'Reset password sent to your email.')
            return redirect('login')
        else:
            messages.error(request, 'Email not found.')
            return render(request, 'reset_password.html')

    return render(request, 'reset_password.html')
