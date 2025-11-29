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

def make_suntimes_frame(
    start : str,
    end : str,
    lat : float,
    lon : float,
    suntimes = [
        'sunrise',
        'sunset',
    ]
):
    """ 
    Create a pandas Dataframe with dates between the specified start and end,
    and columns for the specified suntimes, from the suncalc package.

    Parameters
    ----------
    start : str
        The start date in 'YYYY-MM-DD' format.
    end : str
        The end date in 'YYYY-MM-DD' format.
    lat : float
        Latitude of the location.
    lon : float
        Longitude of the location.
    suntimes : list
        List of suntimes to include as columns in the DataFrame.
    
    Returns
    -------
    df : pd.DataFrame
        DataFrame containing a 'date' column with dates from start to end,
        and columns for the specified suntimes.
    """
    # Verify argument types
    ## Types for `start` and `end` verified in `make_time_frame`
    time_df = make_time_frame(start=start, end=end)
    if not isinstance(lat, (float, int)):
        raise TypeError(f"(make_suntimes_frame) `lat` must be a float or int. Got type: {type(lat)}")
    if not isinstance(lon, (float, int)):
        raise TypeError(f"(make_suntimes_frame) `lon` must be a float or int. Got type: {type(lon)}")
    for suntime in suntimes:
        if not verify_suntime(suntime):
            raise ValueError(f"(make_suntimes_frame) Invalid suntime: {suntime}")
    
    # Get times using suncalc
    suntimes_df = get_times(time_df['date'], [lon]*len(time_df), [lat]*len(time_df))
    # Add specified suntimes to the DataFrame
    for suntime in suntimes:
        # Add to DataFrame
        time_df[suntime] = suntimes_df[suntime]
        # Convert from UTC to local time
        time_df[f"local_{suntime}"] = time_df[suntime].apply(lambda dt: convert_UTC_to_local(dt, lat, lon))
    return time_df

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
