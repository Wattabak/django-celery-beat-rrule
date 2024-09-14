from django.core.exceptions import ValidationError
from django.db import models
from django_celery_beat_rrule.rruleschedule import rruleschedule
from django_celery_beat.models import PeriodicTask


class RruleSchedule(models.Model):
    """Schedule executing on the interval defined as an iCalendar compliant rrule json string"""

    rrule = models.TextField()

    @property
    def schedule(self):
        return rruleschedule(rrule=str(self.rrule))

    def __str__(self):
        return self.rrule.__str__()


class RrulePeriodicTask(PeriodicTask):
    rrule = models.ForeignKey(
        RruleSchedule,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Rrule Schedule",
        help_text="Rrule Schedule to run the task on.  "
        "Set only one schedule type, leave the others null.",
    )

    def __str__(self):
        fmt = "{0.name}: {{no schedule}}"
        if self.interval:
            fmt = "{0.name}: {0.interval}"
        if self.crontab:
            fmt = "{0.name}: {0.crontab}"
        if self.solar:
            fmt = "{0.name}: {0.solar}"
        if self.clocked:
            fmt = "{0.name}: {0.clocked}"
        if self.rrule:
            fmt = "{0.name}: RRULE"
        return fmt.format(self)

    @property
    def schedule(self):
        if self.interval:
            return self.interval.schedule
        if self.crontab:
            return self.crontab.schedule
        if self.solar:
            return self.solar.schedule
        if self.clocked:
            return self.clocked.schedule
        if self.rrule:
            return self.rrule.schedule

    def validate_unique(self, *args, **kwargs):

        schedule_types = ["interval", "crontab", "solar", "clocked", "rrule"]
        selected_schedule_types = [s for s in schedule_types if getattr(self, s)]

        if len(selected_schedule_types) == 0:
            raise ValidationError(
                "One of clocked, interval, crontab, rrule or solar must be set."
            )

        err_msg = "Only one of clocked, interval, crontab, rrule or solar must be set"
        if len(selected_schedule_types) > 1:
            error_info = {}
            for selected_schedule_type in selected_schedule_types:
                error_info[selected_schedule_type] = [err_msg]
            raise ValidationError(error_info)

        # clocked must be one off task
        if self.clocked and not self.one_off:
            err_msg = "clocked must be one off, one_off must set True"
            raise ValidationError(err_msg)

