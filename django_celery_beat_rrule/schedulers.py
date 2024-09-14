from django_celery_beat.schedulers import DatabaseScheduler
from django_celery_beat_rrule.model_entry import RruleModelEntry
from django_celery_beat_rrule.models import RrulePeriodicTask


class RruleDatabaseScheduler(DatabaseScheduler):
    Model = RrulePeriodicTask
    Entry = RruleModelEntry
