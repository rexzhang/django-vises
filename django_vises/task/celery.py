#!/usr/bin/env python

from collections.abc import Sequence
from importlib import import_module
from typing import Any


def autodiscover_schedule(
    installed_app_name_list: Sequence[str],
) -> dict[str, dict[str, Any]]:
    """auto discover schedule
    from:
    {
        'every_minute': [
            {'schedule': crontab(minute='*/1'), 'task': 'esi_db.tasks.demo.demo'},
        ],
    }
    to:<The key words are at both ends>
    {
        'app_name.very_minute.esi_db.tasks.demo.demo': {'schedule': crontab(minute='*/1'), 'task': 'esi_db.tasks.demo.demo'},
    }
    """
    celery_beat_schedule: dict[str, dict[str, Any]] = dict()

    for app_name in installed_app_name_list:
        try:
            celery = import_module(f"{app_name}.celery")
        except ModuleNotFoundError:
            continue

        for group in celery.schedule:
            for entry in celery.schedule[group]:
                name = f"{app_name}.{group}.{entry['task']}"
                celery_beat_schedule[name] = entry

    return celery_beat_schedule
