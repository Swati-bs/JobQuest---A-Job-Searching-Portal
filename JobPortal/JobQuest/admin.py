from django.contrib import admin
from .models import Profile  # Import your model

from django.contrib import admin
from .models import Profile,JobApplication,Job,SavedJob,Notification,Skill,Education,Project

admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(SavedJob)
admin.site.register(Notification)
admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(Project)

