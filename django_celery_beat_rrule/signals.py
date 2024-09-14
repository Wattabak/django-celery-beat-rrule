def signals_connect():
    """Connect to signals."""
    from django.db.models import signals

    from .models import RruleSchedule
    from django_celery_beat.models import PeriodicTasks

    signals.post_save.connect(PeriodicTasks.update_changed, sender=RruleSchedule)
    signals.post_delete.connect(PeriodicTasks.update_changed, sender=RruleSchedule)