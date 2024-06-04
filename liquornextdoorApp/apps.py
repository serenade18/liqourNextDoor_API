from django.apps import AppConfig


class LiquornextdoorappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'liquornextdoorApp'

    def ready(self):
        import liquornextdoorApp.signals  # Import the signals module
