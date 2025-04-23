from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required



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

    path('change-password/', login_required(PasswordChangeView.as_view(template_name='JobQuest/dashboard/change_password.html')), name='change_password'),

    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),

    #Dashboard Features
    path('dashboard/', views.view_dashboard, name='dashboard'),
    path('dashboard/update-profile/',views. update_profile, name='update_profile'),
    path('dashboard/view-profile/', views.view_profile, name='view_profile'),
    path('dashboard/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('dashboard/logout/', views.logout_view, name='logout'),
    path('dashboard/deactivate-account/', views.deactivate_account, name='deactivate_account'),

    path('jobs/', views.job_list, name='job_list'),  # Job listings page
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),  # Job details page
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),  # Job application
    path('my-applications/', views.my_applications, name='my_applications'),  # My Applications page
    path('jobs/save/<int:job_id>/', views.save_job, name='save_job'),
    path('jobs/unsave/<int:job_id>/', views.unsave_job, name='unsave_job'),
    path('jobs/saved/', views.saved_jobs, name='saved_jobs'),

    path('jobs/recommended/', views.recommended_jobs, name='recommended_jobs'),

    path('notifications/', views.notifications, name='notifications'),
    path('notifications/unread-count/', views.unread_notifications_count, name='unread_notifications_count'),

    path('jobapplications/', views.list_job_applications, name='list_job_applications'),
    path('jobapplication/<int:application_id>/update-status/', views.update_job_application_status, name='update_job_application_status'),
    path('create-job/',views.create_job,name='create_job')
]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)