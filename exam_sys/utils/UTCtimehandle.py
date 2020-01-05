import time
from datetime import datetime, tzinfo, timedelta
import pytz


class BeiJingTimezone(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=8)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return '+08:00'

# 没用上
