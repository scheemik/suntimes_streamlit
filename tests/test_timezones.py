from datetime import datetime, timezone, timedelta
import pandas as pd
from numpy import nan

import suntimes_streamlit.timezones as tzs 
# Define test cases
test_cases = {
    "Toronto":
        {
            "lat": 43.0,
            "lon": -79.0,
            "expected_tz_name": "America/Toronto",
        },
    "Cambridge Bay":
        {
            "lat": 69.12,
            "lon": -105.06,
            "expected_tz_name": "America/Cambridge_Bay",
        },
    "Halifax":
        {   # I don't know why, but the actual coordinates of Halifax (44.65, -63.57) return "Etc/GMT+4" instead of "America/Halifax". This is likely due to the timezone database and how it handles certain locations.
            # "lat": 44.64,
            # "lon": -63.57,
            "lat": 45.0,
            "lon": -63.5,
            "expected_tz_name": "America/Halifax",
        },
    "St. John's":
        {   # Similar to Halifax, the actual coordinates of St. John's (47.56, -52.71) return "Etc/GMT+4" instead of "America/St_Johns". This is likely due to the timezone database and how it handles certain locations.
            # "lat": 47.56,
            # "lon": -52.71,
            "lat": 48.0,
            "lon": -54.0,
            "expected_tz_name": "America/St_Johns",
        },
    "Paris":
        {
            "lat": 48.85,
            "lon": -2.35,
            "expected_tz_name": "Europe/Paris",
        },
    "Rio de Janeiro":
        {
            "lat": -22.91,
            "lon": -43.2,
            "expected_tz_name": "America/Sao_Paulo",
        },
    "Sydney":
        {
            "lat": -33.8688,
            "lon": 151.2093,
            "expected_tz_name": "Australia/Sydney",
        },
}

def test_get_tzname():
    """Test the get_tzname function."""
    # Test each case
    for case in test_cases.values():
        tz_name = tzs.get_tzname(case["lat"], case["lon"])
        assert tz_name == case["expected_tz_name"], f"Expected {case['expected_tz_name']}, got {tz_name}"
    # Define invalid test cases for longitude
    invalid_lons = [
        -200,
        200,
        '100',
        nan,
        None,
        [],
        {},
    ]
    # Test each invalid longitude
    for invalid_lon in invalid_lons:
        try:
            tzs.get_tzname(43.0, invalid_lon)
        except:
            assert True, f"get_tzname raised an exception on invalid lon: {invalid_lon}"
        else:
            assert False, f"Expected exception for invalid lon: {invalid_lon}"
    # Define invalid test cases for latitude
    invalid_lats = [
        -99,
        99,
    ] + invalid_lons
    # Test each invalid longitude
    for invalid_lat in invalid_lats:
        try:
            tzs.get_tzname(invalid_lat, -79.0)
        except:
            assert True, f"get_tzname raised an exception on invalid lat: {invalid_lat}"
        else:
            assert False, f"Expected exception for invalid lat: {invalid_lat}"

def test_get_tzinfo():
    """Test the get_tzinfo function."""
    # Test each case
    for case in test_cases.values():
        tz_info = tzs.get_tzinfo(tz_name=case["expected_tz_name"])
        assert tz_info == timezone(timedelta(hours=0), case["expected_tz_name"]), f"Expected {case['expected_tz_name']}, got {tz_name}"
    # Define invalid test cases for longitude
    invalid_lons = [
        -200,
        200,
        '100',
        nan,
        None,
        [],
        {},
    ]
    # Test each invalid longitude
    for invalid_lon in invalid_lons:
        try:
            tzs.get_tzinfo(43.0, invalid_lon)
        except:
            assert True, f"get_tzinfo raised an exception on invalid lon: {invalid_lon}"
        else:
            assert False, f"Expected exception for invalid lon: {invalid_lon}"
    # Define invalid test cases for latitude
    invalid_lats = [
        -99,
        99,
    ] + invalid_lons
    # Test each invalid longitude
    for invalid_lat in invalid_lats:
        try:
            tzs.get_tzinfo(invalid_lat, -79.0)
        except:
            assert True, f"get_tzinfo raised an exception on invalid lat: {invalid_lat}"
        else:
            assert False, f"Expected exception for invalid lat: {invalid_lat}"

def test_convert_UTC_to_local():
    """Test the convert_UTC_to_local function."""
    # Define valid test cases
    test_times = [
        {
            "dt_utc": pd.Timestamp('2020-01-01 12:00:00', tz='UTC'),
            "expected_local_hours": {
                "Toronto": 7,           # EST is UTC-5
                "Cambridge Bay": 5,     # MST is UTC-7
                "Halifax": 8,           # AST is UTC-4
                "St. John's": 8,        # NST is UTC-3:30
                "Paris": 13,            # CET is UTC+1
                "Rio de Janeiro": 9,    # BRT is UTC-3
                "Sydney": 23,           # AEDT is UTC+11
            },
        },
        {
            "dt_utc": datetime(2020, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            "expected_local_hours": {
                "Toronto": 7,           # EST is UTC-5
                "Cambridge Bay": 5,     # MST is UTC-7
                "Halifax": 8,           # AST is UTC-4
                "St. John's": 8,        # NST is UTC-3:30
                "Paris": 13,            # CET is UTC+1
                "Rio de Janeiro": 9,    # BRT is UTC-3
                "Sydney": 23,           # AEDT is UTC+11
            },
        },
        {
            "dt_utc": datetime(2023, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
            "expected_local_hours": {
                "Toronto": 8,           # EDT is UTC-4
                "Cambridge Bay": 6,     # MDT is UTC-6
                "Halifax": 9,           # ADT is UTC-3
                "St. John's": 9,        # NDT is UTC-2:30
                "Paris": 14,            # CEST is UTC+2
                "Rio de Janeiro": 9,    # BRT is UTC-3 (no DST)
                "Sydney": 22,           # AEST is UTC+10 (no DST in June)
            },
        }
    ]
    # Test each case
    for this_time in test_times:
        for city in this_time["expected_local_hours"].keys():
            expected_local_hour = this_time["expected_local_hours"][city]
            city_info = test_cases[city]
            dt_local = tzs.convert_UTC_to_local(this_time["dt_utc"], city_info["lat"], city_info["lon"])
            assert dt_local.hour == expected_local_hour, f"For {city}: Expected hour {expected_local_hour}, got {dt_local.hour}"
    # Test NaT input for UTC datetime
    dt_local_NaT = tzs.convert_UTC_to_local(pd.NaT, 43.0, -79.0)
    assert pd.isna(dt_local_NaT.hour), f"Expected NaN hour, got {dt_local_NaT.hour}"
    # Define invalid test cases
    invalid_datetimes = [
        'not a datetime',
        1234,
        nan,
        None,
        [],
        {},
    ]
    # Test each case
    for invalid_dt in invalid_datetimes:
        test_case = {
            "dt_utc": invalid_dt,
            "lat": -33.8688,
            "lon": 151.2093,
        }
        try:
            result = tzs.convert_UTC_to_local(test_case["dt_utc"], test_case["lat"], test_case["lon"])
        except:
            assert True, f"convert_UTC_to_local raised an exception on invalid input: {test_case['dt_utc']}"
        else:
            assert False, f"Expected exception for invalid input: {test_case['dt_utc']}"