from datetime import datetime, timezone
import pandas as pd
from numpy import nan

import suntimes_streamlit.timezones as tzs 
# Define test cases
test_cases = {
    "Toronto":
        {
            "lat": 43.0,
            "lon": -79.0,
            "expected_tz_name": "America/New_York",
        },
    "Cambridge Bay":
        {
            "lat": 69.12,
            "lon": -105.06,
            "expected_tz_name": "America/Denver",
        },
    "Halifax":
        {
            "lat": 44.64,
            "lon": -63.57,
            "expected_tz_name": "Etc/GMT+4",
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

def test_get_tzinfo():
    """Test the get_tzinfo function."""
    # Test each case
    for case in test_cases.values():
        tz_name, tz_info = tzs.get_tzinfo(case["lat"], case["lon"])
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
    test_cases = [
        {
            "dt_utc": pd.Timestamp('2020-01-01 12:00:00', tz='UTC'),
            "lat": 43.0,
            "lon": -79.0,
            "expected_local_hour": 7,  # EST is UTC-5
        },
        {
            "dt_utc": datetime(2020, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            "lat": 43.0,
            "lon": -79.0,
            "expected_local_hour": 7,  # EST is UTC-5
        },
        {
            "dt_utc": datetime(2023, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
            "lat": -33.8688,
            "lon": 151.2093,
            "expected_local_hour": 22,  # AEST is UTC+10
        },
    ]
    # Test each case
    for case in test_cases:
        dt_local = tzs.convert_UTC_to_local(case["dt_utc"], case["lat"], case["lon"])
        assert dt_local.hour == case["expected_local_hour"], f"Expected hour {case['expected_local_hour']}, got {dt_local.hour}"
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