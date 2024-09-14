# django-celery-beat-rrule

A [django-celery-beat](https://pypi.org/project/django-celery-beat/) plugin that adds a `RruleScheduler`.
It is based on the django-celery-beat's database scheduler and allows running tasks by just creating dateutil's rrule schedules.

# THIS PROJECT IS IN BETA, USE AT YOUR DISCRETION.

# Why?

`Django-celery-beat` is a wonderful library that already includes powerful schedulers like `crontab`, `interval` or `solar`.
But what if your schedule includes irregularities?
If you schedule an event on your calendar you are usually presented with a complex planner that allows you to schedule an event with multiple exceptions, breaks, 
different time intervals that are too complicated to be handled by crontab. This is where `dateutil`'s rrule package comes in,
it allows to easily create complex schedules with groups and exceptions that cover much more ground than crontab.

This project is intended to make this integrating this package easier for running custom events on small to medium scale.

# How it works

A custom rrule-based `DatabaseScheduler` implementation uses an extended periodic task,
that adds a new JSON field storing the serialized rrule schedule. 
Scheduler then is able to pick these tasks up as a regular celery-beat schedule and calculate the next execution date using rrule.after().


## Known issues

1. Potentially poor performance because of the `rrule.after()`'s computational overhead, specifically in complex rules with several exceptions.
2. Underlying issues with how rrule performs validation. There are several issues open on github describing how an RRULE can be created  excluding ALL dates from execution and making their computation take too long.

# Installation

You can install django-celery-beat-rrule either via the Python Package Index (PyPI)
or from source.

To install using `pip`:

```bash
   $ pip install --upgrade django-celery-beat-rrule
```

## Configuration

Add django_celery_beat_rrule to the list of installed apps

```python
INSTALLED_APPS = [
    ...,
    'django_celery_beat_rrule',
]
```

Run django-celery-beat-rrule migrations

```bash
    # make sure you have already installed django-celery-beat's migrations before you run this
    $ python manage.py migrate django_celery_beat_rrule
```

If you change the Django `TIME_ZONE` setting your periodic task schedule
will still be based on the old timezone.

To fix that you would have to reset the "last run time" for each periodic task.