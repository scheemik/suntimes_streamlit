from datetime import datetime, timezone
import pandas as pd
from numpy import nan

import suntimes_streamlit.timezones as tzs 

def test_get_tzinfo():
    """Test the get_tzinfo function."""
    # Define test cases
    test_cases = [
        {
            "lat": 43.0,
            "lon": -79.0,
            "expected_tz_name": "America/New_York",
        },
        {
            "lat": -33.8688,
            "lon": 151.2093,
            "expected_tz_name": "Australia/Sydney",
        }
    ]
    # Test each case
    for case in test_cases:
        tz_name, tz_info = tzs.get_tzinfo(case["lat"], case["lon"])
        assert tz_name == case["expected_tz_name"], f"Expected {case['expected_tz_name']}, got {tz_name}"

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