from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode
from io import BytesIO
from django.core.files import File
import phonenumbers
from phonenumbers import geocoder
from django.core.exceptions import ValidationError




class CustomUser(AbstractUser):
    dob = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    # First name, surname, username, password and email in given from AbstractUser already.


    # Override save method to generate a QR code when saving the user.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        if not self.qr_code:  # Check if QR code doesnt exist yet just for general error prevention.
            qr = qrcode.make(self.username)  # Generate a QR code using the username.
            canvas = BytesIO()
            qr.save(canvas, format='PNG')
            file_name = f'qr_{self.username}.png'
            self.qr_code.save(file_name, File(canvas), save=False)
            super().save(*args, **kwargs)  # Save user again with the QR code.
