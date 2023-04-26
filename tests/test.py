from src.Scrapper import str_to_date,make_request

import datetime

def test_str_to_date():
    assert str_to_date("10-08-2021") == datetime.datetime(2021, 8, 10, 0, 0)

def test_make_request_games():
   assert make_request("https://messi.starplayerstats.com/en/games/0/0/all/0/0/0/t/0/0/0/1") is not None

def test_make_request_goals():
    assert make_request("https://messi.starplayerstats.com/en/goals/0/0/all/0/0/0/t/all/all/0/0/1") is not None
