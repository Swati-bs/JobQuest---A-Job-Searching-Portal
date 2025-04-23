from django.contrib.auth.models import User
from django.db import models
import random
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.core.validators import RegexValidator

   
class Job(models.Model):
    title = models.CharField(max_length=255)  # Job title
    company_name = models.CharField(max_length=255)
    location_type = models.CharField(
        max_length=50,
        choices=[("Remote", "Remote"), ("On-Site", "On-Site"), ("Hybrid", "Hybrid")]
    )
    location = models.CharField(max_length=100, blank=True, null=True)   
    job_type = models.CharField(max_length=50, choices=[("Full-time", "Full-time"), ("Part-time", "Part-time"), ("Internship", "Internship"), ("Contract", "Contract")])
    salary_range = models.CharField(max_length=50, blank=True, null=True)
    experience_level = models.CharField(max_length=50, choices=[("Entry", "Entry"), ("Mid", "Mid"), ("Senior", "Senior")])
    description = models.TextField()
    required_skills = models.TextField()  # Comma-separated skills
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField()
    
    def __str__(self):
        return f"{self.title} at {self.company_name}"
    
class Skill(models.Model):
     skill_name = models.CharField(max_length=100,unique=True)

     def __str__(self):
         return self.skill_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")

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
    skill_entries = models.ManyToManyField(Skill, related_name='profiles')
    recommended_jobs = models.ManyToManyField('Job', related_name='recommended_to', blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',blank=True, null=True)


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

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education_entries')
    degree = models.CharField(max_length=100)
    university = models.CharField(max_length=150)
    graduation_year = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return f"{self.degree} at {self.university}"





class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='project_entries')
    project_title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.project_title
 

class JobApplication(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='job_applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='applications/', blank=True, null=True)  # Allow uploading a custom resume
    cover_letter = models.TextField(blank=True, null=True)  # Optional cover letter
    status = models.CharField(max_length=50, choices=[("Screening", "Screening"), ("Shortlisted", "Shortlisted"), ("Interviewing", "Interviewing"), ("Selected", "Selected"), ("Rejected", "Rejected")], default="Screening")
    applied_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
    # Check for status changes
        if self.pk:  # Object exists
            old_status = JobApplication.objects.get(pk=self.pk).status
            if old_status != self.status:
                # Create notification with updated format
                Notification.objects.create(
                    user=self.profile.user,
                    message=f"Your Job Update for {self.job.title} at {self.job.company_name}!\nYour Application Status: {self.status}."
                )
                from .utils import send_shortlisting_email
                send_shortlisting_email(self.profile.user, self.job, self)

        super().save(*args, **kwargs)  # Call the parent save method

    def __str__(self):
        return f"{self.profile.user.username} applied for {self.job.title}"
    
class SavedJob(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.user.username} saved {self.job.title}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, null=True, blank=True)  # Optional
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
    
    