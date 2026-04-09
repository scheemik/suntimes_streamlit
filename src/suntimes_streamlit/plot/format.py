import pandas as pd
import datetime

def melt_dataset(
    df : pd.DataFrame,
    id_vars : list,
    val_vars : list,
):
    """ Melt a dataset for Altair plotting.

    Stack the specified value variables into a single column, with an additional column to indicate the variable name, for use in Altair plotting.
    
    Parameters
    ----------
    df : `pd.DataFrame`
        The DataFrame to melt.
    id_vars : `list` of `str`
        The columns to use as identifier variables.
    val_vars : `list` of `str`
        The columns to use as value variables.
        
    Returns
    -------
    `pd.DataFrame`
        The melted DataFrame.
    """
    # Verify input arguments
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"(melt_dataset) `df` must be a pandas DataFrame. Got type: {type(df)}")
    if not isinstance(id_vars, list):
        raise TypeError(f"(melt_dataset) `id_vars` must be a list. Got type: {type(id_vars)}")
    else:
        if not all(isinstance(var, str) for var in id_vars):
            raise TypeError(f"(melt_dataset) All elements of `id_vars` must be strings. Got types: {[type(var) for var in id_vars]}")
    if not isinstance(val_vars, list):
        raise TypeError(f"(melt_dataset) `val_vars` must be a list. Got type: {type(val_vars)}")
    else:
        if not all(isinstance(var, str) for var in val_vars):
            raise TypeError(f"(melt_dataset) All elements of `val_vars` must be strings. Got types: {[type(var) for var in val_vars]}")
    
    return df.melt(id_vars=id_vars, value_vars=val_vars, var_name='symbol', value_name='times')

def time_of_day(
    series : pd.Series,
):
    """ Get the time of day from a series of datetimes.
    
    Convert a series of time objects (including tz-aware times) to temporal datetimes for plotting.
    
    Parameters
    ----------
    series : pd.Series
        The series of time objects or tz-aware timestamps.
        
    Returns
    -------
    pd.Series
        The series of temporal datetimes.
    """
    # Verify input arguments
    if not isinstance(series, pd.Series):
        raise TypeError(f"(format_time_of_day) `series` must be a pandas Series. Got type: {type(series)}")
    # Verify that the series contains time objects
    if not all(series.apply(lambda x: isinstance(x, (datetime.time, pd._libs.tslibs.timestamps.Timestamp)) or pd.isna(x))):
        raise TypeError(f"(format_time_of_day) `series` must contain time objects or tz-aware timestamps. Got types: {series.apply(lambda x: type(x)).unique()}")

    return series.apply(lambda t: pd.NaT if pd.isna(t) else datetime.datetime.combine(datetime.datetime(2000, 1, 1), t.replace(tzinfo=None)))