# feedback/apps.py
from django.apps import AppConfig

class FeedbackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feedback'

    def ready(self):
        from .models import Badge
        Badge.create_initial_badges()  # Assurez-vous que cela est bien indenté et dans la méthode ready
