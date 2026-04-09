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
    df : pd.DataFrame
        The DataFrame to melt.
    id_vars : list
        The columns to use as identifier variables.
    val_vars : list
        The columns to use as value variables.
        
    Returns
    -------
    pd.DataFrame
        The melted DataFrame.
    """
    # Verify input arguments
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"(melt_dataset) `df` must be a pandas DataFrame. Got type: {type(df)}")
    if not isinstance(id_vars, list):
        raise TypeError(f"(melt_dataset) `id_vars` must be a list. Got type: {type(id_vars)}")
    if not isinstance(val_vars, list):
        raise TypeError(f"(melt_dataset) `val_vars` must be a list. Got type: {type(val_vars)}")
    
    return df.melt(id_vars=id_vars, value_vars=val_vars, var_name='symbol', value_name='times')