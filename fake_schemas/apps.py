from django.apps import AppConfig


class FakeSchemasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fake_schemas'
