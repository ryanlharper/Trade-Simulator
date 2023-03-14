from django.apps import AppConfig

class PositionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'positions'

    def ready(self):
        import positions.signals