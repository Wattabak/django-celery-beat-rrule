"""Django Application configuration."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

__all__ = ["BeatRruleConfig"]


class BeatRruleConfig(AppConfig):
    """Default configuration for django_celery_beat app."""

    name = "django_celery_beat_rrule"
    label = "django_celery_beat_rrule"
    verbose_name = _("Periodic Tasks")

