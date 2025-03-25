from django.contrib.auth.models import User
from django.db import models
import random
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.core.validators import RegexValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(
            max_length=15,
            blank=True,
            null=True,
            validators=[
                RegexValidator(
                    regex=r'^\+?[1-9]\d{1,14}$',
                    message="Enter a valid phone number.",
                )
            ],
        )
    bio = models.TextField(blank=True, null=True)  # Optional biography field
    location = models.CharField(max_length=100, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    job_preferences = models.CharField(max_length=255, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)  # Comma-separated skills list or JSON



    otp = models.CharField(max_length=6, blank=True, null=True)  # Stores the OTP
    otp_created_at = models.DateTimeField(auto_now=True)  # This field tracks the OTP generation time
    is_email_verified = models.BooleanField(default=False)  # Tracks if email is verified

    def generate_otp(self):
        """Generate and save a random 6-digit OTP"""
        self.otp = f"{random.randint(100000, 999999)}"
        self.otp_created_at = now()  # Update the OTP timestamp
        self.save()

    def is_otp_expired(self):
        """Check if the OTP has expired (0.5 minutes)."""
        expiry_time = self.otp_created_at + timedelta(minutes=0.5)
        return now() > expiry_time
    
    def __str__(self):
        return self.user.username
    
    
