from django.test import TestCase, Client
from gymapp.models import CustomUser, WorkoutSession, Exercise
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


class TrackerTests(TestCase):
    def setUp(self):
        # Creating a user
        self.credentials = {'username': 'testuser', 'password': 'testing100'}
        self.user = get_user_model().objects.create_user(**self.credentials)
        self.client = Client()
        self.client.force_login(self.user)

    def test_add_workout(self):
        url = reverse('add_workout')
        data = {
            'workout_name': 'Testing',
            'date': '2024-04-19'
        }
        # User adds a workout session
        response = self.client.post(url, data)
        # Check redirect after adding.
        # From https://stackoverflow.com/questions/14951356/django-testing-if-the-page-has-redirected-to-the-desired-url
        self.assertEqual(response.status_code, 302)
        # Check if workout session was created.
        self.assertEqual(WorkoutSession.objects.count(), 1)
        self.assertEqual(WorkoutSession.objects.first().workout_name, 'Testing')
    
    def test_add_exercise(self):
        session = WorkoutSession.objects.create(user=self.user, workout_name='Tester Exercise', date='2024-04-19')
        url = reverse('session_detail', args=[session.id])
        data = {
            'name': 'BP',
            'custom_name': '',
            'reps': 10,
            'sets': 3,
            'weight': 100
        }
        response = self.client.post(url, data)
        # Check if successfully added.
        self.assertEqual(response.status_code, 200) 
        # 200 means it stays on the same page.
        # Check if exercise was added to the session.
        self.assertEqual(Exercise.objects.count(), 1)
        self.assertEqual(Exercise.objects.first().name, 'BP')
