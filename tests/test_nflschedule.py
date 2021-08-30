import datetime

import pytest
import random

from nflschedule import *


MIN_SEASON = min(list(SEASON_STARTS.keys()))
MAX_SEASON = max(list(SEASON_STARTS.keys()))
TODAY_DT = datetime.datetime.today().date()


@pytest.fixture
def rseas():
    return random.choice(range(MIN_SEASON, MAX_SEASON + 1))


@pytest.fixture
def rweek():
    return random.choice(range(MIN_WEEK, MAX_WEEK + 1))


def test_schedule_noparams():
    df = schedule()
    assert len(df.season.unique()) >= (MAX_SEASON - MIN_SEASON)
    assert len(df.week.unique()) >= (MAX_WEEK - MIN_WEEK)


def test_schedule_seasparam(rseas):
    df = schedule(season=rseas)
    assert len(df.season.unique()) == 1
    assert len(df.week.unique()) >= (MAX_WEEK - MIN_WEEK)


def test_schedule_weekparam(rweek):
    df = schedule(week=rweek)
    assert len(df.season.unique()) >= (MAX_SEASON - MIN_SEASON)
    assert len(df.week.unique()) == 1


def test_current_week_schedule():
    seas_starts = SEASON_STARTS.get(TODAY_DT.year)
    df = current_week_schedule()
    if (not seas_starts) or (TODAY_DT < seas_starts):
        assert df is None
    else:
        assert df.week.unique() == 1


def test_current_season_schedule():
    seas_starts = SEASON_STARTS.get(TODAY_DT.year)
    df = current_season_schedule()
    if (not seas_starts) or (TODAY_DT < seas_starts):
        assert df is None
    else:
        assert df.week.unique() >= (MAX_WEEK - MIN_WEEK)


def test_current_season():
    """tests current_season"""
    currseas = current_season()
    if currseas is not None:
        assert currseas >= TODAY_DT.year - 1


def test_current_week():
    """tests current_week"""
    week = current_week()
    if week is not None:
        assert MIN_WEEK <= week <= MAX_WEEK


def test_which_season():
    """tests which_season"""
    assert which_season(datetime.date(2020, 9, 30)) == 2020
    assert which_season(datetime.date(2020, 3, 3)) is None
    assert which_season(datetime.date(2020, 1, 2)) == 2019


def test_which_week():
    """tests which_week"""
    assert which_week(datetime.date(2020, 9, 15)) == 1
    assert which_week(datetime.date(2020, 3, 3)) is None
    assert which_week(datetime.date(2020, 10, 29)) == 8
