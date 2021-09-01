# nflschedule/nflschedule/nflschedule.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

"""
Gets schedule information for NFL seasons 1999-

Examples:

# on 9/30/2021
>>>current_season()
2021

# on 8/22/2021
>>>current_season()
None

# on 8/22/2021
>>>current_season(out_of_season=True)
2020

"""
import datetime
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd
from dateutil.parser import parse


logging.getLogger(__name__).addHandler(logging.NullHandler())
DateLike = Union[datetime.datetime, datetime.date, str]
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


def current_season(out_of_season=False):
    """Gets current season (based on today's date)

    Args:
        out_of_season (bool): if True, return most recent season, otherwise return None if out of season.

    Returns:
        int|None

    """
    return which_season(datetime.date.today(), out_of_season)


def current_season_schedule(out_of_season=False):
    """Gets current season schedule (based on today's date)

    Args:
        out_of_season (bool): if True, return most recent season, otherwise return None if out of season.

    Returns:
        DataFrame

    """
    season = current_season(out_of_season)
    if season:
        return schedule(season=season)
    return None


def current_week():
    """Determines season_week of current week"""
    return which_week(datetime.date.today())


def current_week_schedule():
    season = current_season()
    if not season:
        return None
    if datetime.date.today() < SEASON_STARTS.get(season):
        return None
    week = current_week()
    if week <= MAX_WEEK:
        return schedule(season, week)
    return None


def main_slate_count(season: int = None, week: int = None) -> int:
    """Counts games in main slate

    Args:
        season (int): default None
        week (int): default None

    Returns:
        int

    """
    df = schedule(season, week)
    return df.is_main_slate.astype(int).sum()


def main_slate_teams(season: int = None, week: int = None) -> List[str]:
    """Gets teams playing in main slate

    Args:
        season (int): default None
        week (int): default None

    Returns:
        List[str]

    """
    season = season if season else current_season()
    week = week if week else current_week()
    df = schedule(season, week)
    return (
        df.loc[df.is_main_slate, ["home_team", "away_team"]].values.flatten().tolist()
    )


def schedule(
    season: int = None, week: int = None
) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
    """Returns NFL schedule

    Args:
        season (int): default None
        week (int): default None

    Returns:
        pd.DataFrame | List[Dict[str, Any]]

    """
    df = pd.read_csv(DATA_DIR / f"schedule.csv")
    if season and week:
        return df.loc[(df.season == season) & (df.week == week), :]
    if season:
        return df.loc[(df.season == season), :]
    if week:
        return df.loc[(df.week == week), :]
    return df


def season_sundays(
    season: int, as_date: bool = False, fmt: Optional[str] = "%m/%d/%Y"
) -> List[Union[datetime.date, str]]:
    """Gets the regular-season Sundays for a given season

    Args:
        season (int): the season
        as_date (bool): if False, returns dates as str rather than datetime
        fmt (str): the datetime format string, default %m/%d/%Y

    Returns:
        List[Union[datetime.date, str]]

    """
    sundays = []
    start = SEASON_STARTS.get(season)
    sundays.append(start + datetime.timedelta(days=3))
    n_weeks = 17 if season < 2021 else 18
    for _ in range(n_weeks - 1):
        sundays.append(sundays[-1] + datetime.timedelta(7))
    if not as_date:
        return sundays
    try:
        return [datetime.datetime.strftime(d, fmt) for d in sundays]
    except:
        return [datetime.datetime.strftime(d, "%m/%d/%Y") for d in sundays]


def which_season(day: DateLike, out_of_season: bool = False):
    """Determines season of given day

    Args:
        day (DateLike): the day to find season for
        out_of_season (bool): if True, return most recent season, otherwise return None if out of season.

    Returns:
        int|None

    """
    if isinstance(day, str):
        day = parse(day)
    if day.month > 8:
        return day.year
    if day.month < 3:
        return day.year - 1
    if out_of_season:
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
        if delta.days > 0:
            return (delta.days // 7) + 1
    return None
