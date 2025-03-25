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
from .models import Profile
from .forms import CustomUserCreationForm
from django.contrib.messages import get_messages


def register(request):
    storage = get_messages(request)
    for _ in storage:  # Iterate to clear the queue
        pass

    if request.method == 'POST':
        print("DEBUG: POST data:", request.POST)
        print(f"DEBUG: successful post request for registration")

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("DEBUG: Form is valid!")
            user = form.save()  # Save the user instance from the form
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)  # Log in the user automatically

            # Create the profile using get_or_create to avoid duplicates
            profile, created = Profile.objects.get_or_create(user=user)

            # Generate OTP only if the profile is newly created
            if created:
                profile.generate_otp()
                try:
                    send_mail(
                        subject="Email Verification for JobPortal",
                        message=f"Hi {user.username},\n\nYour OTP for JobQuest is {profile.otp}.",
                        from_email="taesberry3112@gmail.com",  # Replace with your email
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    messages.error(request, f"Failed to send email. Error: {e}")
                    return redirect('register')  # Redirect back to registration

            messages.success(request, "Registration successful! Check your email for OTP.")
            return redirect('verify_otp')  # Redirect to OTP verification page
        else:
            print("Registration failed.")
            print("DEBUG: ", form.errors)
            messages.error(request, "Registration failed. Please check the form and try again.")
    else:
        form = CustomUserCreationForm()

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


def resend_otp(request):
    profile = Profile.objects.get(user=request.user)

    if not profile.is_otp_expired():  # Prevent resending OTP before expiry
        return JsonResponse({'success': False, 'message': 'Please wait before resending OTP.'})

    profile.generate_otp()  # Generate and save a new OTP

    # Send the OTP to the user’s email
    send_mail(
        subject="Resend OTP for Email Verification",
        message=f"Hi {request.user.username},\n\nYour new OTP is {profile.otp}.",
        from_email='taesberry3112@gmail.com',
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
    profile = request.user.profile  # Get user's profile

    return render(request, 'JobQuest/dashboard/dashboard.html', {'profile': profile})

@login_required
def logout_confirmation(request):
    profile = request.user.profile  # Get user's profile
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
                from_email="taesberry3112@gmail.com",
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

@login_required
def view_dashboard(request):
    profile = request.user.profile  # Get user's profile
    return render(request, 'JobQuest/dashboard/dashboard.html', {'profile': profile})

from .forms import UpdateProfileForm

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('view_profile')
        else:
            messages.error(request, "Failed to update profile. Please try again.")
    else:
        form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'JobQuest/dashboard/update_profile.html', {'form': form})

@login_required
def view_profile(request):
    profile = request.user.profile  # Assuming Profile is linked to User
    return render(request, 'JobQuest/dashboard/view_profile.html', {'profile': profile})

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

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, get_backends
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

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

