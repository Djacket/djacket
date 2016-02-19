from dateutil import tz
from datetime import datetime
import dateutil.parser as tparser


def time_to_utc(time):
    """
        Returns 'UTC' conversion of the given time in "ISO-8601 like" format.
            'time' is a string data type.
    """

    utc_zone = tz.tzutc()
    dt = tparser.parse(time)
    in_utc = dt.astimezone(utc_zone).strftime("%Y-%m-%dT%H:%M:%S%z")
    return in_utc


def get_year(utc_timestamp):
    """
        Returns year of the given utc timestamp.
    """

    return tparser.parse(utc_timestamp).year


def get_month(utc_timestamp):
    """
        Returns month of the given utc timestamp.
    """

    return tparser.parse(utc_timestamp).month


def get_weeknumber(utc_timestamp):
    """
        Returns week number of the given utc timestamp.
    """

    return tparser.parse(utc_timestamp).isocalendar()[1]


def get_weekday(utc_timestamp):
    """
        Returns week day of the given utc timestamp.
    """

    return tparser.parse(utc_timestamp).isocalendar()[2]
