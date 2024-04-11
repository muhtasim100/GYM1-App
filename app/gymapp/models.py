from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode, datetime, random, phonenumbers
from io import BytesIO
from django.core.files import File
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings

class CustomUser(AbstractUser):
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # First name, surname, username, password and email in given from AbstractUser already.
    
    # Override save method to generate a QR code when saving the user.
    def save(self, *args, **kwargs):        
		# Check if QR code doesnt exist yet just for general error prevention.
        if not self.qr_code:  
            qr = qrcode.make(self.username)  # Generate a QR code using the username.
            canvas = BytesIO()
            qr.save(canvas, format='PNG')
            file_name = f'qr_{self.username}.png'
            self.qr_code.save(file_name, File(canvas), save=False)
            
        super().save(*args, **kwargs)  # Save user with the QR code and phone numeber.

# Details of a session on a date including a name to identify the workout.
class WorkoutSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_sessions')
    # related_name could be useful for querying the database in later functionality.
    date = models.DateField()
    workout_name = models.CharField(max_length=40)  
    # So User can pick personalised name for example, "Leg Day", "Arms + Shoulders" or "CT".
    # 40 char not too long as it can be hard to display. Even this is generous. May need revision.

    # For admin site and good practice. 
    def __str__(self):
        return f"{self.workout_name} on {self.date}"
    
# Model for each exercise in a Workout Session.
class Exercise(models.Model):
    # Some pre made choices so user can select.
    # Eliminates differentiation in capitals/spacing etc. Also why BP, LP, SQ etc is used.
    # May allow charts in future. 
    EXERCISE_CHOICES = [
        ('BP', 'Bench Press'), # Tuple use for database use and displaying the name.
        ('LP', 'Leg Press'),
        ('SQ', 'Squat'),
        ('SP', 'DB Shoulder Press'),
        ('SM', 'Standing Military'),
        ('DL', 'Deadlift'),
        ('PL', 'Pull Ups'),
        ('ID', 'Incline DB'),
        ('IB', 'Incline Barbell'),
        ('OT', 'Other'),  # Allow for custom exercises in case its not in the list.
    ]

    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=100, choices = EXERCISE_CHOICES, default='BP') # Pre made list exercises.
    custom_name = models.CharField(max_length=50, blank=True, null=True)  # User can specify if 'Other' is selected.
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        
    def __str__(self):
        if self.name == 'OT':
            return self.custom_name
        return self.get_name_display()
    
class ExerciseDetail(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='details')
    reps = models.IntegerField()
    sets = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.sets} sets of {self.reps} reps at {self.weight}kg/lb."
    

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    