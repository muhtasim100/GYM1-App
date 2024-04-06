from django.test import TestCase, Client
from gymapp.models import CustomUser, WorkoutSession, Exercise, ExerciseDetail
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal


# Create your tests here.

    
# Test Case 1)
    # CustomUser instance creation.
class CustomUserModelTest(TestCase):
    # Test 1
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
        

# Test Case 2)
        # Login Test
        # Code mostly from user moooeeeep on https://stackoverflow.com/questions/22457557/how-to-test-login-process 
class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        
        get_user_model().objects.create_user(**self.credentials)

    # Test 2
    def test_login(self):
        # Send login data.
        login_url = reverse('login') 
        response = self.client.post(login_url, self.credentials, follow=True)
        # Should be logged in now.
        self.assertTrue(response.context['user'].is_authenticated)
# Test result: passed.




# Test Case 3)
        # Testing the tracker feature and its pages.
class TrackerTests(TestCase):
    def setUp(self):
        # Creating a user.
        self.credentials = {'username': 'testuser', 'password': 'testing100'}
        self.user = get_user_model().objects.create_user(**self.credentials)
        self.client = Client()
        self.client.force_login(self.user)

    # Test 3
        # Testing if user can add a workout session to the tracker.
    def test_add_workout(self):
        url = reverse('add_workout')
        data = {
            'workout_name': 'Testing',
            'date': '2024-04-19'
        }
        # User adds a workout session.
        response = self.client.post(url, data)
        # Check redirect after adding.
        # From https://stackoverflow.com/questions/14951356/django-testing-if-the-page-has-redirected-to-the-desired-url
        self.assertEqual(response.status_code, 302)
        # Check if workout session was created.
        self.assertEqual(WorkoutSession.objects.count(), 1)
        self.assertEqual(WorkoutSession.objects.first().workout_name, 'Testing')
    # Test result: passed.

    # Test 3
        # Test to add an exercise to a workout.
    def test_add_exercise(self):
        session = WorkoutSession.objects.create(user=self.user, workout_name='Tester Exercise', date='2024-04-19')
        url = reverse('add_exercise', args=[session.id])  
        data = {
            'name': 'OT',
            'custom_name': 'Tester'
        }

        response = self.client.post(url, data)

        # Check if the response is a redirect (status code 302) which indicates success.
        self.assertEqual(response.status_code, 302)

        # Check if the exercise was added to the session.
        self.assertEqual(Exercise.objects.count(), 1)
        exercise = Exercise.objects.first()
        self.assertEqual(exercise.name, 'OT')
        self.assertEqual(exercise.custom_name, 'Tester')
        self.assertEqual(exercise.workout_session, session)
    # Test result: passed.


# Test Case 4)
    # Testing the details of an exercise.
class ExerciseDetailTests(TestCase):
    def setUp(self):
        # Creating a user.
        self.user = get_user_model().objects.create_user(username='testuser', password='londonisblue')
        self.client.login(username='testuser', password='londonisblue')
        # Creates a workout session and an exercise for that session.
        self.workout_session = WorkoutSession.objects.create(
            user=self.user,
            date='2024-04-19',
            workout_name='Leg Day'
            )
        self.exercise = Exercise.objects.create(
            workout_session=self.workout_session,
            # 'SQ' for Squats.
            name='SQ', 
            )
        
    # Test 4
        # Testing if automatic set assignment increments properly.
    def test_incrementing_set(self):
        # Creating some "existing" data. Set 1 and 2 added so we can test if new addition is set 3. 
        ExerciseDetail.objects.create(exercise=self.exercise, reps=10, sets=1, weight=Decimal('100.00'))
        ExerciseDetail.objects.create(exercise=self.exercise, reps=8, sets=2, weight=Decimal('120.00'))
        url = reverse('set_info', args=[self.exercise.id])  
        response = self.client.post(url, {'reps': 6, 'weight': '140.00'})
        self.assertEqual(response.status_code, 302)  # Checks if form redirects.

        # Now see if the set number was correctly incremented.
        new_set = ExerciseDetail.objects.latest('id')
        self.assertEqual(new_set.sets, 3)
    # Test result: passed.

    # Test 5
        # Testing if first entry assigns properly a number for the set.
    def test_first_entry(self):
        # Test the first set is saved with set number 1.
        url = reverse('set_info', args=[self.exercise.id])  
        response = self.client.post(url, {'reps': 10, 'weight': '60.00'})
        self.assertEqual(response.status_code, 302) 

        # Check the set number for 1.
        first_set = ExerciseDetail.objects.latest('id')
        self.assertEqual(first_set.sets, 1)
    # Test result: passed.
