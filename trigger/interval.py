__author__ = 'Masutangu'
from trigger.base import BaseTrigger
from datetime import timedelta, datetime
from core.utils import timedelta_seconds, astimezone, convert_to_datetime
from tzlocal import get_localzone
from math import ceil

"""
    quote from apscheduler.trigger
"""

class IntervalTrigger(BaseTrigger):

    def __init__(self, weeks=0, days=0, hours=0, minutes=0, seconds=0, start_date=None, end_date=None, timezone=None):
        self.interval = timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
        self.interval_length = timedelta_seconds(self.interval)
        if self.interval_length == 0:
            self.interval = timedelta(seconds=1)
            self.interval_length = 1

        if timezone:
            self.timezone = astimezone(timezone)
        elif start_date and start_date.tzinfo:
            self.timezone = start_date.tzinfo
        elif end_date and end_date.tzinfo:
            self.timezone = end_date.tzinfo
        else:
            self.timezone = get_localzone()

        start_date = start_date or (datetime.now(self.timezone) + self.interval)
        self.start_date = convert_to_datetime(start_date, self.timezone, 'start_date')
        self.end_date = convert_to_datetime(end_date, self.timezone, 'end_date')

    def get_next_run_time(self, previous_fire_time, curr_time):
        if previous_fire_time:
            next_fire_time = previous_fire_time + self.interval
        elif self.start_date > curr_time:
            next_fire_time = self.start_date
        else:
            timediff_seconds = timedelta_seconds(curr_time - self.start_date)
            next_interval_num = int(ceil(timediff_seconds / self.interval_length))
            next_fire_time = self.start_date + self.interval * next_interval_num

        if not self.end_date or next_fire_time <= self.end_date:
            return self.timezone.normalize(next_fire_time)


    @classmethod
    def create_trigger(cls, **triger_args):
        cls(**triger_args)