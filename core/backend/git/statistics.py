import json
from dateutil import parser
from datetime import datetime

from utils.date import get_year, get_month, get_weeknumber, get_weekday


def extract_month(utc_timestamp):
    """
        Extracts month from utc timestamp string.
    """

    datetime = parser.parse(utc_timestamp)
    return '{0}-{1}'.format(datetime.year, datetime.month)


def extract_day(utc_timestamp):
    """
        Extracts day from utc timestamp string.
    """

    datetime = parser.parse(utc_timestamp)
    return '{0}-{1}-{2}'.format(datetime.year, datetime.month, datetime.day)


class DataPresentation:
    """
        Represents a presentation format for a given dataset (Datasets are python 'dict's basically).
            If data format is 'py' then it's left alone.
            But in case of 'js', a json compatible presentation is returned.
    """

    JS_FORMAT, PY_FORMAT = 'js', 'py'
    VALID_DATA_FORMATS = [JS_FORMAT, PY_FORMAT] # Available data presentation output formats.


    def __init__(self, data_format):
        assert data_format in self.VALID_DATA_FORMATS, 'Input data format is not a valid one.'
        self.data_format = data_format


    def present(self, data):
        """
            Returns presentation of the given dataset.
        """

        if self.data_format == 'js':
            return json.dumps(data)
        elif self.data_format == 'py':
            return data


class GitStatistics:
    """
        Generates data analysis for a git repository. This data will be available
            in python 'dict' or javascript 'json' formats. One can use this statistics
            to plot graphs or analyze repository activities.
    """

    # Available time intervals for generating datasets.
    DAILY_INTERVALS = 'daily'
    WEEKLY_INTERVALS = 'weekly'
    MONTHLY_INTERVALS = 'monthly'
    VALID_DATA_GENERATION_INTERVALS = [DAILY_INTERVALS, WEEKLY_INTERVALS, MONTHLY_INTERVALS]


    def __init__(self, repo, rev):
        self.repo = repo
        self.rev = rev

        self.current_year = datetime.utcnow().isocalendar()[0]
        self.current_week = datetime.utcnow().isocalendar()[1]


    def _for_commits_daily(self, commits):
        """
            Returns number of commits per day for the given commits.
        """

        # get dates only in the current year.
        dates = [extract_day(commit.get_committer_date()) for commit in commits   \
                        if get_year(commit.get_committer_date()) == self.current_year]
        return {date: dates.count(date) for date in dates}


    def _for_commits_weekly(self, commits):
        """
            Returns number of commits per day for the given commits.
        """

        # get dates only in the current year and current week.
        dates = [get_weekday(extract_day(commit.get_committer_date())) for commit in commits  \
                        if get_year(commit.get_committer_date()) == self.current_year and \
                           get_weeknumber(commit.get_committer_date()) == self.current_week]

        return {wd: dates.count(wd) if wd in dates else 0 for wd in range(1, 8)}


    def _for_commits_monthly(self, commits):
        """
            Returns number of commits per month for the given commits.
        """

        dates = [get_month(extract_month(commit.get_committer_date())) for commit in commits
                        if get_year(commit.get_committer_date()) == self.current_year]
        return {mn: dates.count(mn) if mn in dates else 0 for mn in range(1, 13)}


    def for_commits(self, by, data_format):
        """
            Returns dataset for number of commits per given time interval.
        """

        assert by in self.VALID_DATA_GENERATION_INTERVALS, 'Input interval is not a valid one.'

        commits = self.repo.get_commits(self.rev)

        if by == self.DAILY_INTERVALS:
            return DataPresentation(data_format).present(self._for_commits_daily(commits))
        elif by == self.WEEKLY_INTERVALS:
            return DataPresentation(data_format).present(self._for_commits_weekly(commits))
        elif by == self.MONTHLY_INTERVALS:
            return DataPresentation(data_format).present(self._for_commits_monthly(commits))
