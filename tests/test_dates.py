import datetime

from suntimes_streamlit import dates as dts

def test_time_math():
    """Test the time_math function.""" 
    # Define valid test cases
    test_cases = [
        {
            "sourcedate": datetime.date(2020, 1, 31),
            "months": 1,
            "expected_date": datetime.date(2020, 2, 29),  # Leap year
        },
        {
            "sourcedate": datetime.date(2021, 1, 31),
            "months": 1,
            "expected_date": datetime.date(2021, 2, 28),  # Non-leap year
        },
        {
            "sourcedate": datetime.date(2020, 12, 31),
            "months": 2,
            "expected_date": datetime.date(2021, 2, 28),
        },
        {
            "sourcedate": datetime.date(2020, 5, 15),
            "months": -3,
            "expected_date": datetime.date(2020, 2, 15),
        },
        {
            "sourcedate": datetime.date(2020, 1, 31),
            "months": -3,
            "expected_date": datetime.date(2019, 10, 31),
        },
        {
            "sourcedate": datetime.date(2020, 1, 31),
            "months": -4,
            "expected_date": datetime.date(2019, 9, 30),
        },
        {
            "sourcedate": datetime.date(2020, 3, 31),
            "months": -1,
            "expected_date": datetime.date(2020, 2, 29),  # Leap year
        },
    ]
    # Test each case
    for case in test_cases:
        result_date = dts.time_math(case["sourcedate"], months=case["months"])
        assert result_date == case["expected_date"], f"From {case['sourcedate']} with months {case['months']}: Expected {case['expected_date']}, got {result_date}"
    # Define valid test cases with years
    test_cases = [
        {
            "sourcedate": datetime.date(2020, 1, 31),
            "months": 1,
            "years": 4,
            "expected_date": datetime.date(2024, 2, 29),  # Leap year
        },
        {
            "sourcedate": datetime.date(2021, 1, 31),
            "months": 1,
            "years": 1,
            "expected_date": datetime.date(2022, 2, 28),  # Non-leap year
        },
        {
            "sourcedate": datetime.date(2020, 12, 31),
            "months": 2,
            "years": -1,
            "expected_date": datetime.date(2020, 2, 29),
        },
        {
            "sourcedate": datetime.date(2020, 5, 15),
            "months": -3,
            "years": 1,
            "expected_date": datetime.date(2021, 2, 15),
        },
        {
            "sourcedate": datetime.date(2020, 1, 31),
            "months": -3,
            "years": -10,
            "expected_date": datetime.date(2009, 10, 31),
        },
        {
            "sourcedate": datetime.date(2020, 3, 31),
            "months": -1,
            "years": -4,
            "expected_date": datetime.date(2016, 2, 29),  # Leap year
        },
        {
            "sourcedate": datetime.date(2020, 3, 31),
            "months": -1,
            "years": -1,
            "expected_date": datetime.date(2019, 2, 28),  # Non-leap year
        },
    ]
    # Test each case
    for case in test_cases:
        result_date = dts.time_math(case["sourcedate"], months=case["months"], years=case["years"])
        assert result_date == case["expected_date"], f"From {case['sourcedate']} with months {case['months']} and years {case['years']}: Expected {case['expected_date']}, got {result_date}"
    # Define invalid test cases for months
    invalid_months = [ 13, -1, 1.5, "2",  None, [], {} ]
    # Test each invalid month case
    for invalid_month in invalid_months:
        try:
            result = dts.time_math(datetime.date(2020, invalid_month, 1), months=1)
        except (TypeError, ValueError):
            assert True, f"time_math raised exception on invalid month: {invalid_month}, {e}"
        else:
            assert False, f"Expected TypeError for invalid month: {invalid_month}"
    # Define invalid test cases for months to be added
    invalid_months = [ 1.5, "2",  None, [], {} ]
    # Test each invalid month case
    for invalid_month in invalid_months:
        try:
            result = dts.time_math(datetime.date(2020, 1, 1), months=invalid_month)
        except (TypeError, AssertionError) as e:
            assert True, f"time_math raised exception on invalid month: {invalid_month}, {e}"
        else:
            assert False, f"Expected exception for invalid month: {invalid_month}"
    # Define invalid test cases for years
    invalid_years = [ -1, 1.5, "2",  None, [], {} ]
    # Test each invalid year case
    for invalid_year in invalid_years:
        try:
            result = dts.time_math(datetime.date(2020, 1, invalid_year), years=1)
        except (TypeError, ValueError):
            assert True, f"time_math raised exception on invalid year: {invalid_year}, {e}"
        else:
            assert False, f"Expected TypeError for invalid year: {invalid_year}"
    # Define invalid test cases for years to be added
    invalid_years = [ 1.5, "2",  None, [], {} ]
    # Test each invalid year case
    for invalid_year in invalid_years:
        try:
            result = dts.time_math(datetime.date(2020, 1, 1), years=invalid_year)
        except (TypeError, AssertionError) as e:
            assert True, f"time_math raised exception on invalid year: {invalid_year}, {e}"
        else:
            assert False, f"Expected exception for invalid year: {invalid_year}"