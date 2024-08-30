from django.apps import AppConfig

class PizzaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Connexion des signaux lors de l'initialisation de l'application
        from . import signals  # Importer le module des signaux
        from django.conf import settings
        # Vérification du mode de fonctionnement (dev ou prod)
        if settings.DEBUG:
            print("L'application est en mode développement.")
        else:
            print("L'application est en mode production.")
