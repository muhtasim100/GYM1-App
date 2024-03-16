from django.test import TestCase
from gymapp.models import CustomUser

# Create your tests here.

class CustomUserModelTest(TestCase):
    
    # CustomUser instance
    def test_create(self):
        user = CustomUser.objects.create_user(
            username='fakeuser', 
            email='test@test.com',
            password='userisfake123',
            dob='2001-01-01', 
            address='10 Downing Street', 
            phone_number='+447723566330'
        )

        user.save()

        self.assertEqual(CustomUser.objects.count(),1)
        self.assertEqual(CustomUser.objects.first().username, 'fakeuser')
        self.assertEqual(CustomUser.objects.first().email, 'test@test.com')
        self.assertEqual(CustomUser.objects.first().dob.isoformat(), '2001-01-01')
        self.assertEqual(CustomUser.objects.first().address, '10 Downing Street')
        self.assertTrue(CustomUser.objects.first().qr_code)  

        
