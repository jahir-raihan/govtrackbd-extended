from django.apps import AppConfig


class GeoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'geo_app'

    def ready(self):
        from .updater import start
        start()
