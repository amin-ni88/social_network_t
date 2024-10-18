from django.test import TestCase
from time import time
# Create your tests here.


class SocialTesting(TestCase):
    def setUp(self):
        pass
    
    # def test_status_url(self):
    #     request = self.client.get("/")
    #     self.assertEqual(request.status_code , 200)

    def test_404(self):
        request = self.client.get("ERitrokmM/")
        self.assertEqual(request.status_code , 404)