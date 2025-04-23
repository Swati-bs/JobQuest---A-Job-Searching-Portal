from django.apps import AppConfig


class JobquestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'JobQuest'
    
    def ready(self):
        import JobQuest.signals 
