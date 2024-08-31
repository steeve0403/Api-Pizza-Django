from django.apps import AppConfig

class PizzaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from django.conf import settings
        if settings.DEBUG:
            print("The application is in development mode.")
        else:
            print("The application is in production mode.")
