from datetime import timezone, tzinfo, timedelta, datetime
from timezonefinder import TimezoneFinderL, data
tf = TimezoneFinderL(in_memory=True)
from pandas import Timestamp, NaT
from numpy import nan

# Get a list of all the timezone names from the timezonefinder data
from importlib import resources as impresources

timezone_txt = impresources.files(data) / 'timezone_names.txt'
with timezone_txt.open("rt") as f:
    # Read in the file as a list of lines
    timezone_list = f.read().splitlines()

def get_tzname(
    lat: float,
    lon: float,
):
    """ Get the name of the timezone.

    For a given longitude and latitude, return the name of the timezone. 
    If no timezone is found, return "UTC".

    Parameters
    ----------
    lat : float
        Latitude of the location.
    lon : float
        Longitude of the location.
    
    Returns
    -------
    tz_name : str
        Timezone name.
    
    Examples
    --------
    >>> get_tzname(43.0, -79.0)
    'America/Toronto'
    """
    # Verify argument types
    if not isinstance(lat, (float, int)):
        raise TypeError(f"(get_tzname) `lat` must be a float or int. Got type: {type(lat)}")
    if not isinstance(lon, (float, int)):
        raise TypeError(f"(get_tzname) `lon` must be a float or int. Got type: {type(lon)}")
    # Verify that latitude and longitude are within valid ranges
    if not (-90 <= lat <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if not (-180 <= lon <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees.")
    # Get the timezone name
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    # If no timezone is found, default to UTC
    if isinstance(tz_name, type(None)):
        tz_name = "UTC"
    return tz_name

def get_tzinfo(
    tz_name: str = None,
    lat: float = None,
    lon: float = None,
):
    """ Get the tzinfo object for a given longitude and latitude.

        Parameters
        ----------
        tz_name : `str`, `None`, optional
            Timezone name. If provided, `lat` and `lon` are ignored.
        lat : `float`, `None`, optional
            Latitude of the location.
        lon : `float`, `None`, optional
            Longitude of the location.
        
        Returns
        -------
        tz_name : str
            Timezone name.
        tz_info : tzinfo
            Timezone info object.
        
        Examples
        --------
        >>> get_tz(43.0, -79.0)
        tzinfo(<DstTzInfo 'America/Toronto' EDT-1 day, 20:00:00 DST>)
    """
    # Verify argument types
    if isinstance(tz_name, type(None)):
        if not isinstance(lat, (float, int)):
            raise TypeError(f"(get_tzinfo) `lat` must be a float or int. Got type: {type(lat)}")
        if not isinstance(lon, (float, int)):
            raise TypeError(f"(get_tzinfo) `lon` must be a float or int. Got type: {type(lon)}")
        # Get the timezone name
        tz_name = get_tzname(lat, lon)
    elif not isinstance(tz_name, str):
        raise TypeError(f"(get_tzinfo) `tz_name` must be a string or `None`. Got type: {type(tz_name)}")
    else:
        if tz_name not in timezone_list:
            raise ValueError(f"(get_tzinfo) `tz_name` must be a valid timezone name. Got: {tz_name}")
    # Get the timezone info object
    tz_info = timezone(timedelta(hours=0), tz_name)
    return tz_info

def convert_UTC_to_local(
    dt_utc: datetime,
    tz_name: str = None,
    lat: float = None,
    lon: float = None,
):
    """ Convert UTC to local time.

    Convert a UTC datetime to local time based on the given latitude and longitude.

    Parameters
    ----------
    dt_utc : datetime
        The datetime in UTC to be converted.
    tz_name : `str`, `None`, optional
        Timezone name. If provided, `lat` and `lon` are ignored.
    lat : `float`, `None`, optional
        The latitude of the location.
    lon : `float`, `None`, optional
        The longitude of the location.
    
    Returns
    -------
    dt_local : datetime
        The datetime converted to local time.
    """
    # Verify argument types
    if isinstance(dt_utc, datetime):
        # Convert to pd.Timestamp as this allows the conversion to work
        dt_utc = Timestamp(dt_utc)
    if isinstance(dt_utc, type(NaT)):
        # Return the given time if input is Not a Time
        return dt_utc
    if not isinstance(dt_utc, Timestamp):
        raise TypeError(f"(convert_UTC_to_local) `dt_utc` must be a Timestamp object. Got type: {type(dt_utc)}")
    if not isinstance(tz_name, type(None)):
        if not isinstance(tz_name, str):
            raise TypeError(f"(convert_UTC_to_local) `tz_name` must be a string or `None`. Got type: {type(tz_name)}")
        elif tz_name not in timezone_list:
            raise ValueError(f"(convert_UTC_to_local) `tz_name` must be a valid timezone name. Got: {tz_name}")
        else:
            local_name = tz_name
    else:
        local_name = get_tzname(lat, lon)
    # Note: `get_tzinfo()` verifies lat and lon are valid types and in valid ranges
    # Get the local timezone info
    local_info = get_tzinfo(tz_name=local_name, lat=lat, lon=lon)
    # Get the UTC timezone info
    utc_info = timezone(timedelta(hours=0), "UTC")

    # Assign the UTC timezone info to the given datetime
    dt_utc = dt_utc.replace(tzinfo=utc_info)
    # Convert from UTC to local time
    try:
        dt_local = dt_utc.astimezone(local_name)
    except:
        dt_local = dt_utc.astimezone(local_info)
    return dt_local