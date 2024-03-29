from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode, datetime, random, phonenumbers
from io import BytesIO
from django.core.files import File
from phonenumbers import geocoder
from phonenumbers import PhoneNumberFormat
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # email
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # First name, surname, username, password and email in given from AbstractUser already.
    
    # Override save method to generate a QR code when saving the user.
    def save(self, *args, **kwargs):
        if self.phone_number: # For error prevention and robustness.
            try:
                parsed_phone = phonenumbers.parse(self.phone_number, "GB")
                if not phonenumbers.is_valid_number(parsed_phone):
                    raise ValueError('Invalid phone number format')
                # If valid, format the phone number in E.164 format for 2FA text.
                self.phone_number = phonenumbers.format_number(parsed_phone, PhoneNumberFormat.E164)
            except phonenumbers.NumberParseException:
                raise ValidationError("The phone number entered is not valid.")
				# No need to say if valid because it will just be accepted.
        
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
    

    
