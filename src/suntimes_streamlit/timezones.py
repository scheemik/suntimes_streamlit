from datetime import timezone, tzinfo, timedelta, datetime
from timezonefinder import TimezoneFinderL
tf = TimezoneFinderL(in_memory=True)

def get_tzinfo(
    lat: float,
    lon: float,
):
    """ 
    Get the tzinfo object for a given longitude and latitude.

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
    tz_info : tzinfo
        Timezone info object.
    
    Examples
    --------
    >>> get_tz(43.0, -79.0)
    'America/Toronto'
    """
    # Verify argument types
    if not isinstance(lat, (float, int)):
        raise TypeError(f"(convert_UTC_to_local) `lat` must be a float or int. Got type: {type(lat)}")
    if not isinstance(lon, (float, int)):
        raise TypeError(f"(convert_UTC_to_local) `lon` must be a float or int. Got type: {type(lon)}")
    # Verify that latitude and longitude are within valid ranges
    if not (-90 <= lat <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if not (-180 <= lon <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees.")
    # Get the timezone name
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    # 
    tz_info = timezone(timedelta(hours=0), tz_name)
    return tz_name, tz_info

def convert_UTC_to_local(
    dt_utc: datetime,
    lat: float,
    lon: float,
):
    """ 
    Convert a UTC datetime to local time based on the given latitude and longitude.

    Parameters
    ----------
    dt_utc : datetime
        The datetime in UTC to be converted.
    lat : float
        The latitude of the location.
    lon : float
        The longitude of the location.
    
    Returns
    -------
    dt_local : datetime
        The datetime converted to local time.
    """
    # Verify argument types
    if not isinstance(dt_utc, datetime):
        raise TypeError(f"(convert_UTC_to_local) `dt_utc` must be a datetime object. Got type: {type(dt_utc)}")
    if not isinstance(lat, (float, int)):
        raise TypeError(f"(convert_UTC_to_local) `lat` must be a float or int. Got type: {type(lat)}")
    if not isinstance(lon, (float, int)):
        raise TypeError(f"(convert_UTC_to_local) `lon` must be a float or int. Got type: {type(lon)}")
    
    # Get the local timezone info
    local_name, local_info = get_tzinfo(lat, lon)
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