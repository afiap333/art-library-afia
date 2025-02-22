from django.apps import AppConfig


class ArtlibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'artlibrary'
    def ready(self):
        import artlibrary.signals
