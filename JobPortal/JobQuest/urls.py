from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView,LoginView


urlpatterns = [
    path('', views.home, name='home'),  
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('protected/', views.protected_view, name='protected_view'),  # Example protected route
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Redirect to the homepage after logout
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),  # Define the login route
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    
]
