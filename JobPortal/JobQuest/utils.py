# utils.py
from django.core.mail import send_mail
from .models import Notification  # Import models as needed
def send_recommendation_notifications(user, jobs):
    for job in jobs:
        Notification.objects.create(
            user=user,
            message=f"New job: {job.title} at {job.company_name}. Check it out now!"
        )
    if jobs.exists():
        job_list = "\n".join([f"{job.title} at {job.company_name}" for job in jobs])
        send_mail(
            'New Job Recommendations',
            f"Hi {user.first_name},\n\nCheck out these new jobs:\n\n{job_list}\n\nBest regards,\nJobQuest Team",
            'admin_email@example.com',
            [user.email],
            fail_silently=False
        )

def send_shortlisting_email(user, job, job_application):
    try:
        # Send an email
        send_mail(
            f'Job Update! for {job.title} at {job.company_name}',
            f"Hi {user.first_name},\n\nYou have been {job_application.status} for {job.title} at {job.company_name}.\n\nGood luck!\nJobQuest Team",
            'example@example.com',
            [user.email],
            fail_silently=False,
        )

    except Exception as e:
        print(f"ERROR: Failed to send email - {e}")