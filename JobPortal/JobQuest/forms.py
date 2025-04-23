from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from .models import Profile


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'bio',
            'location',
            'resume',
            'linkedin',
            'portfolio',
            'github',
            'profile_picture',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a short bio about yourself'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your location'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter your LinkedIn URL'}),
            'portfolio': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter your portfolio URL'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter your GitHub profile URL'}),
            'profile_picture': forms.FileInput(attrs={'accept': 'image/*'}),
        }
        # help_texts = {
        #     'resume': 'Upload your resume in PDF format.',
        # }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        print(resume.name)
        if resume and not resume.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed for resumes.")
        return resume
    

# job details entry form - for convenience
from django import forms
from .models import Job  # Import your Job model

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_name', 'location', 'location_type', 'job_type', 
                  'experience_level', 'salary_range', 'description', 'application_deadline']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'title': 'Job Title',
            'company_name': 'Company Name',
            'location': 'Location (City, State)',
            'location_type': 'Location Type (e.g., Remote, On-Site, Hybrid)',
            'job_type': 'Job Type (e.g., Full-time, Part-time)',
            'experience_level': 'Experience Level',
            'salary_range': 'Salary Range',
            'description': 'Job Description',
            'application_deadline': 'Application Deadline',
        }