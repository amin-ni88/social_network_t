from django.test import TestCase
from time import time
from django.shortcuts import reverse
from account  import models 
model = models.Profile 
from django.contrib.auth.models import User

class SocialTesting(TestCase):
    def setUp(self):
        model.objects.create(
            password= '1234' , 
            mobile = '09901234567' , 
            user = User.objects.create(username='test1'),
            email ='test@gmail.com',
            otp = '1238' , 
            bio = 'BIO' , 
            location = '0.99881323',
        )
        model.objects.check(
            password= '1234' , 
            mobile = '09901234567' , 
            user = User.objects.all()[0],
            email ='test@gmail.com',
            otp = '1238' , 
            bio = 'BIO' , 
            location = '0.99881323',
        )
    
    def test_status_url(self): # تست صحت صفحه نخست
        request = self.client.get("/")
        self.assertEqual(request.status_code , 200)

    def test_404(self): # تست خطای 404 در صورت عدم وجود url
        request = self.client.get("ERitrokmM/")
        self.assertEqual(request.status_code , 404)

    def test_load_time(self): # تست زمان لود صفحه (مد نظر 1.7 ثانیه زمان ببرد)
        start_load = time()
        request = self.client.get("/")
        end_load = time()
        load_time = end_load - start_load 
        self.assertLess(load_time , 1.7)

    def test_api_auth_url(self): # تست صحت صفحه api-auth/
        request = self.client.get("api-auth/")
        self.assertEqual(request.status_code , 200)

    def test_url_by_name(self): # تست اسم url
        requests = self.client.get(reverse("login_attempt"))
        self.assertEqual(requests.status_code , 200)
        
        

    