from django.test import TestCase
from time import time
# Create your tests here.


class SocialTesting(TestCase):
    def setUp(self):
        pass
    
    # def test_status_url(self): # تست صحت صفحه نخست
    #     request = self.client.get("/")
    #     self.assertEqual(request.status_code , 200)

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
        

    