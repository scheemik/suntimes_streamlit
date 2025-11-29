from datetime import datetime, timezone

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

