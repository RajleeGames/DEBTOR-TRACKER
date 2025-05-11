from django.apps import AppConfig

class DebtsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'debts'

    def ready(self):
        from django.contrib.auth.models import User
        from .models import Profile

        # Define a safe method to get profile
        def get_profile(user):
            try:
                return user.profile
            except Profile.DoesNotExist:
                return None

        # Attach to User model
        setattr(User, 'get_profile', get_profile)
