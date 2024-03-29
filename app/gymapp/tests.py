from django.test import TestCase
from gymapp.models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

class CustomUserModelTest(TestCase):
    
# Test 1)
    # CustomUser instance creation.
    def test_create(self):
        user = CustomUser.objects.create_user(
            username='fakeuser', 
            email='test@test.com',
            password='userisfake123',
        )

        user.save()

    # Checking if instance created.
        self.assertEqual(CustomUser.objects.count(),1)
        self.assertEqual(CustomUser.objects.first().username, 'fakeuser')
        self.assertEqual(CustomUser.objects.first().email, 'test@test.com')
        self.assertEqual(CustomUser.objects.first().dob.isoformat(), '2001-01-01')
        self.assertEqual(CustomUser.objects.first().address, '10 Downing Street')
        self.assertTrue(CustomUser.objects.first().qr_code)  
    # Test result: passed.
        
# Test 2)
        # Login Test
        # Code mostly from user moooeeeep on https://stackoverflow.com/questions/22457557/how-to-test-login-process 
class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        get_user_model().objects.create_user(**self.credentials)
    def test_login(self):
        # send login data
        login_url = reverse('login') 
        response = self.client.post(login_url, self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)
