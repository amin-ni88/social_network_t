from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
import random
from django.contrib.auth import authenticate, login, logout
import http.client
from django.views import View
from django.conf import settings
from django.contrib.auth import authenticate, login
import http.client
import json
import logging
from django.conf import settings
from kavenegar import *
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import update_session_auth_hash
from .forms import ConfirmTempPasswordForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import string
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm, EmailLoginForm



def send_otp(request,mobile,otp):
    otp= random.randint(1000,9999)
    api = KavenegarAPI('75673944714D35384C516B76624D3637632F42616F5445334767776254496341664F75534F642F486538593D')
    params = {
        'sender': ' ',  # Use a verified sender
        'receptor': "09382446363",
        'message': f'otp:{otp}'
}
    otp = request.POST.get('otp')
    profile = Profile.objects.filter(mobile=mobile).first()
        
    if otp == profile.otp:
            return redirect('cart')
    else:
            print('Wrong')
            
    try:
        response = api.sms_send(params)
        print(response)
    except Exception as e:
        print(f"Error: {e}")

class CustomLogoutView(View):
    def get(self, request):
        logout(request)



def login_attempt(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        user = User.objects.filter(profile__mobile=mobile).first()
        if user:
            login(request, user)
            return redirect('cart')  # Redirect to the home page
        else:
            return render(request, 'login.html', {'error': 'Invalid mobile number', 'form': LoginForm()})
    return render(request, 'login.html', {'form': LoginForm()})


def email_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            login(request, user)
            return redirect('cart')  # Redirect to the home page
        else:
            return render(request, 'email_login.html', {'error': 'Invalid email or password', 'form': EmailLoginForm()})
    return render(request, 'email_login.html', {'form': EmailLoginForm()})


   
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        check_user = User.objects.filter(email=email).first()
        check_profile = Profile.objects.filter(mobile=mobile).first()

        if check_user or check_profile:
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'register.html', context)

        user = User(email=email, first_name=name, username=name)
        user.set_password(password)
        user.save()
        otp = str(random.randint(1000, 9999))
        profile = Profile(user=user, mobile=mobile, otp=otp)
        profile.save()
        send_otp(request, mobile, otp)
        request.session['mobile'] = mobile
        login(request, user)  # Log in the user
        return redirect('cart')  # Redirect to the profile page
    return render(request, 'register.html')


def otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        
        if otp == profile.otp:
            return redirect('cart')
        else:
            print('Wrong')
            
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'otp.html' , context)
            
        
    return render(request,'otp.html' , context)


@login_required
def profile(request, username):
    if request.user.username != username:
        return redirect('cart')

    user = User.objects.get(username=username)
    profile = user.profile

    if request.method == "POST":
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        profile.mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        if password:
            user.set_password(password)
            user.save()
            # Re-authenticate the user after changing the password
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cart')  # Redirect to the home page after password change
            else:
                print("Re-authentication failed")
        else:
            user.save()
            profile.save()

        return redirect('profile', username=user.username)

    return render(request, 'profile.html', {'user': user, 'profile': profile})




def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                user.set_password(temp_password)
                user.save()

                subject = "Password Reset Requested"
                email_template_name = "password/password_reset_email.txt"
                c = {
                    "email": user.email,
                    'domain': request.get_host(),
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    'temp_password': temp_password
                }
                email_content = render_to_string(email_template_name, c)
                email = EmailMessage(subject, email_content, 'sard.zarei00@gmail.com', [user.email])
                email.send(fail_silently=False)
            return redirect('confirm_temp_password', uid=urlsafe_base64_encode(force_bytes(user.pk)), token=default_token_generator.make_token(user))
    return render(request, "password/password_reset.html")





from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_decode

def confirm_temp_password(request, uid, token):
    if request.method == "POST":
        temp_password = request.POST.get('temp_password')
        new_password = request.POST.get('new_password')
        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
            if default_token_generator.check_token(user, token):
                if user.check_password(temp_password):
                    print("Temporary password matched")
                    user.set_password(new_password)
                    user.save()
                    # Re-authenticate the user with the new password
                    user = authenticate(username=user.username, password=new_password)
                    if user is not None:
                        login(request, user)
                        return redirect('cart')  # Redirect to the home page
                    else:
                        print("Re-authentication failed")
                else:
                    print("Temporary password did not match")
            else:
                print("Token mismatch")
        except User.DoesNotExist:
            print("User does not exist")
            return redirect('login')  # Redirect to login if the user does not exist
    return render(request, "password/confirm_temp_password.html")





