import pandas as pd
from suncalc import get_times

from suntimes_streamlit.timezones import convert_UTC_to_local

def make_time_frame(
    start : str,
    end : str,
):
    """ 
    Create a pandas DataFrame with dates between the specified start and end.

    Parameters
    ----------
    start : str
        The start date in 'YYYY-MM-DD' format.
    end : str
        The end date in 'YYYY-MM-DD' format.
    
    Returns
    -------
    df : pd.DataFrame
        DataFrame containing a 'date' column with dates from start to end.
    """
    # Verify argument types
    if not isinstance(start, str):
        raise TypeError(f"(make_time_frame) `start` must be a string. Got type: {type(start)}")
    if not isinstance(end, str):
        raise TypeError(f"(make_time_frame) `end` must be a string. Got type: {type(end)}")
    # Verify the date format
    try:
        pd.to_datetime(start)
    except ValueError:
        raise ValueError(f"(make_time_frame) `start` must be in 'YYYY-MM-DD' format. Got value: {start}")
    try:
        pd.to_datetime(end)
    except ValueError:
        raise ValueError(f"(make_time_frame) `end` must be in 'YYYY-MM-DD' format. Got value: {end}")
    
    # Create the DataFrame
    df = pd.DataFrame({'date': pd.date_range(start=start, end=end)})
    return df

def verify_suntime(
    suntime : str,
):
    """ 
    Verify that the provided suntime is included in the suncalc.get_times output.

    Parameters
    ----------
    suntime : str
        The suntime name to verify.
    
    Returns
    -------
    bool
        True if the suntime is valid, False otherwise.
    """
    # Verify argument type
    if not isinstance(suntime, str):
        raise TypeError(f"(verify_suntime) `suntime` must be a string. Got type: {type(suntime)}")
    
    # Create list of valid suntimes
    valid_suntimes = [
        'solar_noon',
        'nadir',
        'sunrise',
        'sunset',
        'sunrise_end',
        'sunset_start',
        'dawn',
        'dusk',
        'nautical_dawn',
        'nautical_dusk',
        'night_end',
        'night',
        'golden_hour_end',
        'golden_hour',
    ]
    # Check whether the given suntime is in the above list
    if suntime in valid_suntimes:
        return True
    else:
        return False
