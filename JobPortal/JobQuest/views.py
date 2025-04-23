from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from .models import Profile
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from .models import Profile,Education,Skill,Project
from .forms import CustomUserCreationForm
from django.contrib.messages import get_messages
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import login

def register(request):
    # Clear any previous messages in the queue
    storage = get_messages(request)
    for _ in storage:
        pass

    if request.method == 'POST':
        print("DEBUG: POST data:", request.POST)
        print("DEBUG: Successful POST request for registration")

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("DEBUG: Form is valid!")
            user = form.save()  # Save the user instance from the form
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Authenticate user
            login(request, user)  # Log the user in

            # Create or retrieve Profile instance
            profile, created = Profile.objects.get_or_create(user=user)
            print(f"DEBUG: Profile object = {profile}")
            print(f"DEBUG: Profile created status = {created}")

            # Generate OTP regardless of creation status
            profile.generate_otp()
            print("DEBUG: OTP generated =", profile.otp)

            try:
                # Send OTP email
                send_mail(
                    subject="Email Verification for JobPortal",
                    message=f"Hi {user.username},\n\nYour OTP for JobQuest is {profile.otp}.",
                    from_email="example@example.com",  # Replace with your email
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                print("DEBUG: Registration email verification OTP sent...")
                messages.success(request, "Registration successful! Check your email for OTP.")
            except Exception as e:
                print(f"DEBUG: Failed to send email. Error: {e}")
                messages.error(request, f"Failed to send email. Error: {e}")
                return redirect('register')  # Redirect back to registration

            return redirect('verify_otp')  # Redirect to OTP verification page
        else:
            print("DEBUG: Registration failed:", form.errors)
            messages.error(request, "Registration failed. Please check the form and try again.")
    else:
        form = CustomUserCreationForm()  # Display empty form for GET requests

    return render(request, 'registration/register.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_profile = get_object_or_404(Profile, user=request.user)

        if user_profile.otp == otp:
            user_profile.is_email_verified = True
            user_profile.save()
            messages.success(request, "Your email has been verified! You can now access your account.")
            return redirect('home')  # Redirect to the home/dashboard page
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'registration/verify_otp.html')

from django.http import JsonResponse

from django.shortcuts import render
from datetime import datetime

def about_us(request):
    return render(request, 'JobQuest/about_us.html', {
        'current_year': datetime.now().year,  
    })

from django.shortcuts import render
from datetime import datetime

def privacy_policy(request):
    return render(request, 'JobQuest/privacy_policy.html', {
        'current_year': datetime.now().year,
    })

from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Sending an email (or log the submission for now)
        try:
            send_mail(
                subject=f"JobQuest-Contact Us: {subject}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=email,
                recipient_list=['example@mexample.com'],
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'JobQuest/contact_us.html', {
        'current_year': datetime.now().year,
    })

def resend_otp(request):
    profile = Profile.objects.get(user=request.user)

    if not profile.is_otp_expired():  # Prevent resending OTP before expiry
        return JsonResponse({'success': False, 'message': 'Please wait before resending OTP.'})

    profile.generate_otp()  # Generate and save a new OTP

    # Send the OTP to the user’s email
    send_mail(
        subject="Resend OTP for Email Verification",
        message=f"Hi {request.user.username},\n\nYour new OTP is {profile.otp}.",
        from_email='example@example.com',
        recipient_list=[request.user.email],
    )
    
    return JsonResponse({'success': True, 'message': 'A new OTP has been sent to your email.'})


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def protected_view(request):
    if not request.user.profile.is_email_verified:
        messages.warning(request, "You must verify your email to access this page.")
        return redirect('verify_otp')

    return render(request, 'protected_page.html')

from django.shortcuts import render

@login_required
def home(request):
    profile = request.user.profile  

    return render(request, 'JobQuest/dashboard/dashboard.html', {'profile': profile})

@login_required
def logout_confirmation(request):
    profile = request.user.profile 
    return render(request, 'JobQuest/dashboard/logout_confirmation.html', {'profile': profile})

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def logout_view(request):
    logout(request)  # Logs out the user by clearing their session
    messages.success(request, "You have been logged out successfully!")  
    return redirect('login')  # Redirect to the login page

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def logout_view(request):
    if request.method == "POST":  # Ensure logout is triggered only via POST requests for security
        logout(request)
        messages.success(request, "You have been logged out successfully!")
        return redirect('login')  # Redirect to login page
    else:
        messages.error(request, "Logout failed. Please try again.")
        return redirect('home')  # Redirect somewhere else if logout fails
    
    
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)
            profile.generate_otp()  # Generate a new OTP
            send_mail(
                subject="Password Reset OTP",
                message=f"Hi {user.username},\n\nYour OTP for password reset is {profile.otp}.",
                from_email="example@example.com",
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, "OTP sent to your email. Please check.")
            return redirect('verify_password_otp')  # Redirect to OTP verification page
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
    return render(request, 'registration/forgot_password.html')

from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)  # Set up logging

def verify_password_otp(request):
    if request.method == 'POST':
        # Logging the start of the process
        logger.info("Entered password reset OTP block")

        # Retrieve the OTP and email from the POST request
        otp = request.POST.get('otp')
        email = request.POST.get('email')

        # Validate that both OTP and email are provided
        if not otp or not email:
            messages.error(request, "Please provide both email and OTP.")
            return render(request, 'registration/verify_password_otp.html')

        try:
            # Attempt to fetch the User object using the provided email
            user = User.objects.get(email=email)
            logger.debug(f"User found: {user}")

            # Attempt to fetch the Profile object associated with the User
            profile = Profile.objects.get(user=user)
            logger.debug(f"Profile found for user: {profile}")

            # Verify that the OTP matches the stored value
            if profile.otp == otp:  # Use secure OTP comparison in production
                messages.success(request, "OTP verified! You can now reset your password.")
                logger.info("OTP verified! Redirecting to reset password page.")
                return redirect(reverse('reset_password'))  # Use dynamic URL resolution
            else:
                messages.error(request, "Invalid OTP. Please try again.")
        except User.DoesNotExist:
            # Handle case where user doesn't exist
            logger.warning("No user found with the provided email.")
            messages.error(request, "No user found with this email.")
        except Profile.DoesNotExist:
            # Handle case where profile doesn't exist
            logger.warning("No profile associated with the user.")
            messages.error(request, "No profile associated with this user.")
        except Exception as e:
            # Handle any unexpected exceptions
            logger.error(f"Unexpected error occurred: {e}")
            messages.error(request, "An error occurred while verifying OTP. Please try again.")

    # Render the OTP verification page for GET requests or after an error
    print("not an post request")
    return render(request, 'registration/verify_password_otp.html')

from django.contrib.auth.models import User

def reset_password(request):
    storage = get_messages(request)
    for _ in storage:  # Iterate to clear the queue
        pass

    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)  # Update password securely
                user.save()
                messages.success(request, "Password reset successful. You can now log in.")
                return redirect('login')  # Redirect to login page
            except User.DoesNotExist:
                messages.error(request, "No user found with this email.")
        else:
            messages.error(request, "Passwords do not match. Please try again.")
    return render(request, 'registration/reset_password.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required
# def view_dashboard(request):
#     profile = request.user.profile  
#     return render(request, 'JobQuest/dashboard/dashboard.html', {'profile': profile})

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def unread_notifications_count(request):
    unread_count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'unread_count': unread_count})

@login_required
def view_dashboard(request):
    profile = request.user.profile

    # Fetch unread notifications dynamically
    unread_notifications = request.user.notifications.filter(is_read=False)
    unread_count = unread_notifications.count()

    return render(request, 'JobQuest/dashboard/dashboard.html', {
        'profile': profile,
        'unread_notifications': unread_notifications,
        'unread_count': unread_count,  # Pass the count to the template
    })

import cv2
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from JobQuest.models import Profile, Education, Skill, Project
from .forms import UpdateProfileForm

@login_required
def update_profile(request):
    profile = request.user.profile  # Access the user's profile

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)  # Save basic form fields without committing to DB yet

            # Handle webcam photo (base64 string)
            webcam_photo = request.POST.get('webcam_photo')
            if webcam_photo:
                try:
                    # Decode the base64 string
                    format, imgstr = webcam_photo.split(';base64,')
                    ext = format.split('/')[-1]  # Get file extension (e.g., jpeg)
                    decoded_img = base64.b64decode(imgstr)

                    # Save the photo to the profile picture field
                    profile.profile_picture.save(f'webcam_photo_{profile.user.username}.{ext}', ContentFile(decoded_img), save=False)
                except Exception as e:
                    messages.error(request, f"Error saving webcam photo: {e}")

            # Handle manually uploaded profile picture
            if 'profile_picture' in request.FILES:
                uploaded_picture = request.FILES['profile_picture']

                # Temporarily save the image to validate it using OpenCV
                temp_file_path = default_storage.save('temp.jpg', uploaded_picture)
                image = cv2.imread(temp_file_path)

                if image is None:
                    messages.error(request, "Invalid image. Please upload a valid photo.")
                else:
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                    if len(faces) == 0:
                        messages.error(request, "No face detected in the uploaded image. Please upload a clear face photo.")
                    else:
                        profile.profile_picture = uploaded_picture  # Save the valid profile picture

            # Save the profile
            profile.save()
            form.save_m2m()  # Save ManyToMany relationships like skills

            # Handle dynamic entries for Education
            education_degrees = request.POST.getlist('education-degree[]')
            education_universities = request.POST.getlist('education-university[]')
            education_years = request.POST.getlist('education-year[]')

            for degree, university, year in zip(education_degrees, education_universities, education_years):
                if degree and university:  # Only save valid entries
                    Education.objects.update_or_create(
                        profile=profile, degree=degree, university=university,
                        defaults={'graduation_year': year}
                    )

            # Handle dynamic entries for Skills
            skills = request.POST.getlist('skills-name[]')
            for skill_name in skills:
                if skill_name:  # Save valid skills only
                    skill, created = Skill.objects.get_or_create(skill_name=skill_name)
                    profile.skill_entries.add(skill)  # Associate the skill with the profile

            # Handle dynamic entries for Projects
            project_titles = request.POST.getlist('project-title[]')
            project_descriptions = request.POST.getlist('project-description[]')

            for title, description in zip(project_titles, project_descriptions):
                if title:  # Save valid projects only
                    Project.objects.update_or_create(
                        profile=profile, project_title=title,
                        defaults={'description': description}
                    )

            # Success message and redirect to the profile view
            messages.success(request, "Profile updated successfully!")
            return redirect('view_profile')
        else:
            messages.error(request, "Failed to update profile. Please try again.")
    else:
        # Initialize the form with the current profile data
        form = UpdateProfileForm(instance=profile)

    return render(request, 'JobQuest/dashboard/update_profile.html', {'form': form})


@login_required
def view_profile(request):
    profile = request.user.profile  # Get the user's Profile object
    educations = profile.education_entries.all()  # Fetch all related Education entries
    skills = profile.skill_entries.all()  # Fetch all related Skill entries
    projects = profile.project_entries.all()  # Fetch all related Project entries

    return render(request, 'JobQuest/dashboard/view_profile.html', {
        'profile': profile,
        'educations': educations,
        'skills': skills,
        'projects': projects,
    })

from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'JobQuest/dashboard/change_password.html'  # Correct path to the template
    success_message = "Your password was successfully updated!"
    success_url = '/dashboard/'  # Redirect to dashboard after password update

@login_required
def deactivate_account(request):
    storage = get_messages(request)
    for _ in storage:  # Iterate to clear the queue
        pass
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.save()
        return redirect('logout')
    return render(request, 'JobQuest/dashboard/deactivate_account.html')



from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_backends

def reactivate_account(request):
    storage = get_messages(request)
    for _ in storage:  # Clear the message queue
        pass

    if request.method == 'POST':
        print("DEBUG: Post request for reactivating account")
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"DEBUG: Entered post, {username}, {password}")

        try:
            # Try to get the user even if inactive
            user = User.objects.get(username=username)
            if not user.is_active:  # Check if the account is inactive
                if user.check_password(password):  # Verify the password manually
                    print("DEBUG: User is not active but password is correct")

                    # Reactivate the account
                    user.is_active = True
                    user.save()

                    # Set the backend explicitly
                    backend = get_backends()[0]  # Get the first authentication backend
                    user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

                    messages.success(request, "Your account has been reactivated successfully!")
                    login(request, user)  # Log in the user
                    return redirect('dashboard')  # Redirect to dashboard
                else:
                    print("DEBUG: Password is incorrect")
                    messages.error(request, "Invalid credentials. Please try again.")
            else:
                print("DEBUG: User is already active")
                messages.error(request, "Your account is already active.")
        except User.DoesNotExist:
            print("DEBUG: User doesn't exist")
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, 'JobQuest/dashboard/reactivate_account.html')



from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, JobApplication, SavedJob
from django.db.models import Q

@login_required
def job_list(request):
    # Fetch all jobs initially
    jobs = Job.objects.all()

    # Get search query and filter parameters from the request
    search_query = request.GET.get('search', '').strip()
    location_type_filter = request.GET.get('location', '')
    location_city_filter = request.GET.get('location_city', '')  # New city filter
    min_salary = request.GET.get('min_salary')
    max_salary = request.GET.get('max_salary')
    job_type_filter = request.GET.get('job_type', '')
    experience_filter = request.GET.get('experience_level', '')


    # Apply search and filter conditions
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(company_name__icontains=search_query)
        )
    if location_type_filter:
        jobs = jobs.filter(location_type=location_type_filter)

        # Apply city filter if location type is NOT "Remote"
        if location_type_filter != 'Remote' and location_city_filter:
            jobs = jobs.filter(location__icontains=location_city_filter)
    if min_salary and min_salary.isdigit():
        jobs = jobs.filter(salary_range__gte=min_salary)  # Filter jobs with salary >= min_salary
    if max_salary and max_salary.isdigit():
        jobs = jobs.filter(salary_range__lte=max_salary)  # Filter jobs with salary <= max_salary
    if job_type_filter:
        jobs = jobs.filter(job_type=job_type_filter)
    if experience_filter:
        jobs = jobs.filter(experience_level=experience_filter)

    return render(request, 'JobQuest/jobs/job_list.html', {
        'jobs': jobs,
        'search_query': search_query,
        'location_filter': location_type_filter,
        'city_filter': location_city_filter,
        'min_salary': min_salary,
        'max_salary': max_salary,
        'job_type_filter': job_type_filter,
        'experience_filter': experience_filter,
    })
    
@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if the user has applied for the job using the profile field
    user_profile = request.user.profile  # Assuming a Profile model is linked to the User model
    user_applied = JobApplication.objects.filter(profile=user_profile, job=job).exists()
    is_saved = SavedJob.objects.filter(profile=request.user.profile, job=job).exists()
    
    return render(request, 'JobQuest/jobs/job_detail.html', {
        'job': job,
        'user_applied': user_applied,  # Pass the status to the template
        'is_saved': is_saved,
    })

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    profile = request.user.profile
    if request.method == 'POST':
        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter')
        JobApplication.objects.create(profile=profile, job=job, resume=resume, cover_letter=cover_letter)
        return redirect('job_detail', job_id=job_id)
    return render(request, 'JobQuest/jobs/apply_job.html', {'job': job})

@login_required
def saved_jobs(request):
    saved_jobs = SavedJob.objects.filter(profile=request.user.profile).select_related('job')  # Optimize query
    return render(request, 'JobQuest/jobs/saved_jobs.html', {'saved_jobs': saved_jobs})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
def save_job(request, job_id):
    profile = request.user.profile  # Retrieve the user's profile
    job = get_object_or_404(Job, id=job_id)  # Get the job

    # Check if the job is already saved
    if SavedJob.objects.filter(profile=profile, job=job).exists():
        messages.info(request, "You have already saved this job.")
    else:
        SavedJob.objects.create(profile=profile, job=job)
        messages.success(request, "Job saved successfully!")

    return redirect('job_detail', job_id=job_id)

@login_required
def unsave_job(request, job_id):
    profile = request.user.profile
    job = get_object_or_404(Job, id=job_id)

    saved_job = SavedJob.objects.filter(profile=profile, job=job)
    if saved_job.exists():
        saved_job.delete()
        messages.success(request, "Job removed from saved jobs.")
    else:
        messages.info(request, "This job is not in your saved list.")

    return redirect('job_detail', job_id=job_id)

@login_required
def my_applications(request):
    # Fetch all job applications for the logged-in user's profile
    applications = JobApplication.objects.filter(profile=request.user.profile).select_related('job')
    return render(request, 'JobQuest/jobs/my_applications.html', {'applications': applications})


from django.db.models import Q
from .models import Job
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from . recommendations import create_job_recommendation_notifications

@login_required
def recommended_jobs(request):
    profile = request.user.profile
    user_skills = profile.skill_entries.all().values_list('skill_name', flat=True)

    if not user_skills:  # Check if the user has no skills
        return render(request, 'JobQuest/jobs/recommended_jobs.html', {
            'recommended_jobs': [],  # No recommendations
        })

    query = Q()
    for skill in user_skills:
        query |= Q(required_skills__icontains=skill)

    recommended_jobs = Job.objects.filter(query)
    new_recommended_jobs = recommended_jobs.exclude(id__in=profile.recommended_jobs.values_list('id', flat=True))
    profile.recommended_jobs.add(*new_recommended_jobs)

    if new_recommended_jobs.exists():
        from .utils import send_recommendation_notifications
        send_recommendation_notifications(profile.user, new_recommended_jobs)

    return render(request, 'JobQuest/jobs/recommended_jobs.html', {
        'recommended_jobs': recommended_jobs,
    })


from .models import Notification, Job

@login_required
def notifications(request):
    # Fetch all notifications
    notifications = request.user.notifications.all().order_by('-created_at')

    # Mark all notifications as read persistently
    if request.method == "POST" or 'mark_read' in request.GET:  # Trigger marking on an action
        notifications.filter(is_read=False).update(is_read=True)
        return redirect('dashboard') 

    return render(request, 'JobQuest/notifications.html', {
        'notifications': notifications,
    })

# job details entry form - for convenience

from django.shortcuts import render, redirect
from .forms import JobForm
from django.contrib import messages

@login_required
def create_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            # Additional processing, if needed
            job.save()
            messages.success(request, "Job has been successfully created!")
            return redirect('job_list')  # Redirect to the job listing page
    else:
        form = JobForm()

    return render(request, 'JobQuest/jobs/create_job.html', {'form': form})

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from JobQuest.models import JobApplication

def update_job_application_status(request, application_id):
    # Fetch the specific job application
    application = get_object_or_404(JobApplication, pk=application_id)

    if request.method == 'POST':
        # Get new status from the form data
        new_status = request.POST.get('status')
        if new_status in ['Screening', 'Shortlisted', 'Interviewing', 'Selected', 'Rejected']:
            application.status = new_status
            application.save()
            messages.success(request, f"Status updated to '{new_status}' successfully!")
        else:
            messages.error(request, "Invalid status update.")
        return redirect('list_job_applications')  # Redirect back to the list view

    # Render the update form
    return render(request, 'JobQuest/job_application_update.html', {'application': application})

from django.shortcuts import render
from JobQuest.models import JobApplication

def list_job_applications(request):
    # Fetch all job applications from the database
    applications = JobApplication.objects.select_related('profile', 'job').all()
    return render(request, 'JobQuest/job_application_list.html', {'applications': applications})