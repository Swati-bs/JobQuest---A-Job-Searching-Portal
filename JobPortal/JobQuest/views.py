from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from .models import Profile
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            profile = Profile.objects.create(user=user)
            profile.generate_otp()

            send_mail(
                subject="Email Verification for JobPortal",
                message=f"Hi {user.username},\n\nYour  OTP for JobQuest is {profile.otp}.",
                from_email="taesberry3112@gmail.com",  # Replace with your email
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(request, "Registration successful! Check your email for OTP.")
            return redirect('verify_otp')  # Redirect to OTP verification page
        else:
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
    return render(request, 'home.html', {'username': request.user.username})

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