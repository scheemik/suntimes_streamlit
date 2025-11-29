import pandas as pd

from suntimes_streamlit import time_arrays as tarrs

def test_make_time_frame():
    """Test the make_time_frame function."""
    # Define test cases
    test_cases = [
        {
            "start": "2020-01-01",
            "end": "2020-01-10",
            "expected_length": 10,
        },
        {
            "start": "2020-01-01",
            "end": "2020-12-31",
            "expected_length": 366,
        },
        {
            "start": "2020-01-01",
            "end": "2024-12-31",
            "expected_length": 1827,
        },
    ]
    # Test each case
    for case in test_cases:
        # Create a time frame
        df = tarrs.make_time_frame(start=case["start"], end=case["end"])
        # Verify the length of the DataFrame
        assert len(df) == case["expected_length"], f"Expected {case['expected_length']} days, got {len(df)}"
        # Verify the first and last dates
        assert df['date'].iloc[0] == pd.Timestamp(case["start"]), f"Expected start date {case['start']}, got {df['date'].iloc[0]}"
        assert df['date'].iloc[-1] == pd.Timestamp(case["end"]), f"Expected end date {case['end']}, got {df['date'].iloc[-1]}"

def test_verify_suntime():
    """Test the verify_suntime function."""
    # Define valid suntimes
    valid_suntimes = [
        'sunrise',
        'sunset',
        'dawn',
        'dusk',
    ]
    # Test valid suntimes
    for suntime in valid_suntimes:
        assert tarrs.verify_suntime(suntime) == True, f"Expected {suntime} to be valid."
    # Define invalid suntimes
    invalid_suntimes = [
        'invalid_time',
        1234,
        42.0,
        None,
        True,
        {},
        [],
    ]
    # Test invalid suntimes
    for suntime in invalid_suntimes:
        try:
            result = tarrs.verify_suntime(suntime)
            assert result == False, f"Expected {suntime} to be invalid."
            continue
        except TypeError:
            assert True, f"verify_suntime raised an exception on invalid input: {e}"
        else:
            assert False, f"verify_suntime did not raise an exception on invalid input: {suntime}"