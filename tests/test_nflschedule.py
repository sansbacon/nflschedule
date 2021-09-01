import datetime

from freezegun import freeze_time
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


def test_current_season():
    """tests current_season"""
    currseas = current_season()
    if currseas is None:
        currseas = current_season(True)
    assert currseas >= TODAY_DT.year - 1


@freeze_time("2020-09-14")
def test_current_season_schedule_frozen():
    """Tests current_season_schedule"""
    df = current_season_schedule()
    assert 2020 in df.season.values


def test_current_season_schedule():
    """Tests current_season_schedule"""
    df = current_season_schedule(True)
    assert current_season(True) in df.season.values


@freeze_time("2020-09-14")
def test_current_week_frozen():
    """Tests current_season_schedule"""
    assert current_week() == 1


def test_current_week():
    """tests current_week"""
    week = current_week()
    if week is not None:
        assert MIN_WEEK <= week <= MAX_WEEK


@freeze_time("2020-09-14")
def test_current_week_schedule_frozen():
    df = current_week_schedule()
    assert df.week.nunique() == 1


@freeze_time("2021-08-14")
def test_current_week_schedule():
    df = current_week_schedule()
    assert df is None


def test_main_slate_count():
    """Tests main_slate_count"""
    season = 2020
    week = 1
    assert main_slate_count(season, week) == 12


def test_main_slate_teams():
    """Tests main_slate_teams"""
    season = 2020
    week = 1
    t = main_slate_teams(season, week)
    assert len(t) == main_slate_count(season, week) * 2
    assert "CHI" in t


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


def test_season_sundays():
    """Tests season_sundays"""
    ss = season_sundays(2020)
    assert len(ss) == 17
    assert isinstance(ss[0], datetime.date)


def test_season_sundays_return_str():
    """Tests season_sundays"""
    ss = season_sundays(2020, as_date=False, fmt="%Y-%m-%d")
    assert len(ss) == 17
    dstr = ss[0]
    assert isinstance(dstr, str)
    assert dstr[0:4] == "2020"
    assert "-" in dstr


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
