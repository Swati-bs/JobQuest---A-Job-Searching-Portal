from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

# @receiver(user_logged_in)
# def fetch_unread_notifications(sender, request, user, **kwargs):
#     unread_count = user.notifications.filter(is_read=False).count()
#     print(f"DEBUG: Unread notifications after login for {user.username} -> {unread_count}")

@receiver(user_logged_in)
def trigger_recommendation_notifications(sender, request, user, **kwargs):
    print(f"DEBUG: User Logged In - {user.username}")
    from .recommendations import create_job_recommendation_notifications
    create_job_recommendation_notifications(user)


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job, Profile
@receiver(post_save, sender=Job)
def notify_users_on_new_job(sender, instance, created, **kwargs):
    if created:
        print(f"DEBUG: New Job Added - {instance.title}")
        profiles = Profile.objects.all()
        from .recommendations import create_job_recommendation_notifications
        for profile in profiles:
            create_job_recommendation_notifications(profile.user)