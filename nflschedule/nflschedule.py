"""
nflschedule.py

Gets schedule information

"""
import datetime
from functools import lru_cache
import logging
import math
from pathlib import Path

import pandas as pd


logging.basicConfig(level=logging.INFO)
DATA_DIR = Path(__file__).parent / "data"
MIN_WEEK = 1
MAX_WEEK = 18
SEASON_STARTS = {
    1999: datetime.date(1999, 9, 12),
    2000: datetime.date(2000, 9, 3),
    2001: datetime.date(2001, 9, 9),
    2002: datetime.date(2002, 9, 5),
    2003: datetime.date(2003, 9, 4),
    2004: datetime.date(2004, 9, 9),
    2005: datetime.date(2005, 9, 8),
    2006: datetime.date(2006, 9, 7),
    2007: datetime.date(2007, 9, 6),
    2008: datetime.date(2008, 9, 4),
    2009: datetime.date(2009, 9, 10),
    2010: datetime.date(2010, 9, 9),
    2011: datetime.date(2011, 9, 8),
    2012: datetime.date(2012, 9, 5),
    2013: datetime.date(2013, 9, 5),
    2014: datetime.date(2014, 9, 4),
    2015: datetime.date(2015, 9, 10),
    2016: datetime.date(2016, 9, 8),
    2017: datetime.date(2017, 9, 7),
    2018: datetime.date(2018, 9, 6),
    2019: datetime.date(2019, 9, 5),
    2020: datetime.date(2020, 9, 10),
    2021: datetime.date(2021, 9, 9),
}


def current_season():
    return which_season(datetime.date.today())


@lru_cache(maxsize=None)
def current_season_schedule():
    season = current_season()
    if season:
        return schedule(season=season)
    return None


def current_week(season=None):
    """Determines season_week of current week"""
    return which_week(datetime.date.today())


@lru_cache(maxsize=None)
def current_week_schedule():
    season = current_season()
    if season:
        week = current_week()
        if week <= MAX_WEEK:
            return schedule(season, week)
    return None


@lru_cache(maxsize=None)
def main_slate_teams(season=None, week=None):
    season = season if season else current_season()
    week = week if week else current_week()
    df = schedule(season, week)
    return df.loc[df.is_main_slate, :].tolist()


@lru_cache(maxsize=None)
def schedule(season=None, week=None):
    df = pd.read_csv(DATA_DIR / f"schedule.csv")
    if season and week:
        return df.loc[(df.season == season) & (df.week == week), :]
    if season:
        return df.loc[(df.season == season), :]
    if week:
        return df.loc[(df.week == week), :]
    return df


def which_season(day):
    """Determines season of given day

    Args:
        day (datetime): the day to find season for

    Returns:
        int

    """
    if day.month > 8:
        return day.year
    if day.month < 3:
        return day.year - 1
    return None


def which_week(day):
    """Determines season week of given day

    Args:
        day (datetime): the day to find season for

    Returns:
        int

    """
    season = which_season(day)
    if season:
        delta = day - SEASON_STARTS[season]
        return math.floor(delta.days / 7) + 1
    return None
