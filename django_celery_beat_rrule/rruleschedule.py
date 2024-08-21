from datetime import datetime, timedelta, timezone
from logging import getLogger
from typing import Union, Optional, Callable

from celery import Celery
from celery.schedules import BaseSchedule, schedstate
from celery.utils.time import remaining
from dateutil.rrule import rrule, rruleset


from .rrule_serializer import rruleset_to_str

logger = getLogger(__name__)


class rruleschedule(BaseSchedule):
    def __init__(
        self,
        rrule: Union[rrule, rruleset],
        nowfun: Optional[Callable] = None,
        app: Optional[Celery] = None,
    ):
        self.rrule = rrule
        super().__init__(nowfun=nowfun, app=app)

    @property
    def rrulestring(self) -> str:
        return rruleset_to_str(self.rrule)

    def next_date(self, last_run_at: datetime) -> Optional[datetime]:
        return self.rrule.after(last_run_at, inc=False)

    def remaining_estimate(self, last_run_at: datetime) -> Optional[timedelta]:
        """Always assume rrules are naive datetimes, any operations on them should be regarded as such"""
        last_run_at = last_run_at.replace(tzinfo=None)
        next_date = self.next_date(last_run_at=last_run_at)
        logger.debug(
            f"Calculating remaining estimate for {self.rrulestring}"
            f"next_date is {next_date}"
        )
        return (
            remaining(last_run_at, next_date - last_run_at, datetime.now(tz=None), True)
            if next_date is not None
            else None
        )

    def is_due(self, last_run_at: datetime) -> schedstate:
        """Return tuple of ``(is_due, next_time_to_check)``.

        Notes:
            - next time to check is in seconds.

            - ``(True, 20)``, means the task should be run now, and the next
                time to check is in 20 seconds.

            - ``(False, 12.3)``, means the task is not due, but that the
              scheduler should check again in 12.3 seconds.

        The next time to check is used to save energy/CPU cycles,
        it does not need to be accurate but will influence the precision
        of your schedule.  You must also keep in mind
        the value of :setting:`beat_max_loop_interval`,
        that decides the maximum number of seconds the scheduler can
        sleep between re-checking the periodic task intervals.  So if you
        have a task that changes schedule at run-time then your next_run_at
        check will decide how long it will take before a change to the
        schedule takes effect.  The max loop interval takes precedence
        over the next check at value returned.

        .. admonition:: Scheduler max interval variance

            The default max loop interval may vary for different schedulers.
            For the default scheduler the value is 5 minutes, but for example
            the :pypi:`django-celery-beat` database scheduler the value
            is 5 seconds.
        """
        last_run_at = last_run_at or datetime.now(tz=None) - timedelta(seconds=5)
        last_run_at = last_run_at.replace(tzinfo=None)
        rem_delta = self.remaining_estimate(last_run_at)
        if rem_delta is None:
            # rrule reached its final date, reschedule far into the future
            max_date = datetime.max.replace(tzinfo=None)
            return schedstate(
                is_due=False, next=(max_date - last_run_at).total_seconds()
            )
        remaining_s = max(rem_delta.total_seconds(), 0)
        logger.debug(remaining_s)
        if remaining_s == 0:
            next_rem_delta = self.remaining_estimate(
                self.next_date(last_run_at=last_run_at)
            )
            if not next_rem_delta:
                # rrule reached its final date, reschedule far into the future
                max_date = datetime.max.replace(tzinfo=None)
                return schedstate(
                    is_due=True, next=(max_date - last_run_at).total_seconds()
                )
            logger.debug(f"Remaining delta and running the scheduler, {next_rem_delta}")
            next_remaining_s = max(next_rem_delta.total_seconds(), 0)
            return schedstate(is_due=True, next=next_remaining_s)
        return schedstate(is_due=False, next=remaining_s - 25)
