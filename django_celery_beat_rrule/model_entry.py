from celery import schedules
from django_celery_beat.clockedschedule import clocked
from django_celery_beat.models import (
    CrontabSchedule,
    IntervalSchedule,
    SolarSchedule,
    ClockedSchedule,
)
from django_celery_beat.schedulers import ModelEntry

from django_celery_beat_rrule.models import RruleSchedule
from django_celery_beat_rrule.rruleschedule import rruleschedule


class RruleModelEntry(ModelEntry):
    model_schedules = (
        (schedules.crontab, CrontabSchedule, "crontab"),
        (schedules.schedule, IntervalSchedule, "interval"),
        (schedules.solar, SolarSchedule, "solar"),
        (clocked, ClockedSchedule, "clocked"),
        (rruleschedule, RruleSchedule, "rrule"),
    )
