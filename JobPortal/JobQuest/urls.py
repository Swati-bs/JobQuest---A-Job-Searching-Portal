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
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-password-otp/', views.verify_password_otp, name='verify_password_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('logout-confirmation/', views.logout_confirmation, name='logout-confirmation'),
    path('reactivate-account/', views.reactivate_account, name='reactivate_account'),



    #Dashboard Features
    path('dashboard/', views.view_dashboard, name='dashboard'),
    path('dashboard/update-profile/',views. update_profile, name='update_profile'),
    path('dashboard/view-profile/', views.view_profile, name='view_profile'),
    path('dashboard/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('dashboard/logout/', views.logout_view, name='logout'),
    path('dashboard/deactivate-account/', views.deactivate_account, name='deactivate_account'),

]
