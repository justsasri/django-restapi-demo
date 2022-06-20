from django.apps import AppConfig
from django.core.management import call_command
from django.db.models.signals import post_migrate


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self) -> None:
        post_migrate.connect(init_app, sender=self)
        return super().ready()


def init_app(sender, **kwargs):
    call_command("init_demo_users")
