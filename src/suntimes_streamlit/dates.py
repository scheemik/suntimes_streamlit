import datetime
import calendar

def time_math(
    sourcedate : datetime.date, 
    years : int = 0,
    months : int = 0,
):
    """ 
    Add or subtract years and months from a given date.

    Writen because datetime.timedelta does not support months or years.

    Parameters
    ----------
    sourcedate : datetime.date
        The original date.
    years : int
        Number of years to add (can be negative).
    months : int
        Number of months to add (can be negative).
    
    Returns
    -------
    new_date : datetime.date
        The new date after adding / subtracting the specified years and months.
    """
    # Verify argument types
    if not isinstance(sourcedate, datetime.date):
        raise TypeError(f"(time_math) `sourcedate` must be a datetime object. Got type: {type(sourcedate)}")
    if not isinstance(years, int):
        raise TypeError(f"(time_math) `years` must be an int. Got type: {type(years)}")
    if not isinstance(months, (float, int)):
        raise TypeError(f"(time_math) `months` must be an int. Got type: {type(months)}")

    # Calculate the new year and month
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12 + years
    month = month % 12 + 1
    # Adjust the day if it exceeds the number of days in the new month
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)