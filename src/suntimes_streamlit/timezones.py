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
