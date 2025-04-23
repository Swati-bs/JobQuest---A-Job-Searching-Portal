# recommendations.py
from .models import Job, Notification
from django.core.mail import send_mail

def create_job_recommendation_notifications(user):
    profile = user.profile
    user_skills = profile.skill_entries.all().values_list('skill_name', flat=True)

    matching_jobs = Job.objects.filter(
        required_skills__icontains=user_skills
    ).exclude(
        id__in=Notification.objects.filter(
            user=user, message__icontains="New job:"
        ).values_list('job_application__job_id', flat=True)
    )

    new_notifications = []
    job_list = []

    for job in matching_jobs:
        notification = Notification(
            user=user,
            message=f"New job: {job.title} at {job.company_name}. Check it out now!"
        )
        new_notifications.append(notification)
        job_list.append(f"{job.title} at {job.company_name}")

    if new_notifications:
        Notification.objects.bulk_create(new_notifications)

    if job_list:
        send_mail(
            'New Job Recommendations',
            f"Hi {user.first_name},\n\nCheck out these jobs matching your skills:\n\n" +
            "\n".join(job_list) +
            "\n\nBest regards,\nJobQuest Team",
            'example@example.com',
            [user.email],
            fail_silently=False,
        )