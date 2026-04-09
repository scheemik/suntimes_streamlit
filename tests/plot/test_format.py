import pandas as pd
import datetime

from suntimes_streamlit import plot as sun_plts

def test_melt_dataset():
    """Test the melt_dataset function."""
    # Create a sample DataFrame
    df = pd.DataFrame({
        'date': pd.date_range(start='2020-01-01', end='2020-01-03'),
        'sunrise': pd.to_datetime(['2020-01-01 07:00:00', '2020-01-02 07:01:00', '2020-01-03 07:02:00']),
        'sunset': pd.to_datetime(['2020-01-01 17:00:00', '2020-01-02 17:01:00', '2020-01-03 17:02:00']),
    })
    # Melt the DataFrame
    melted_df = sun_plts.format.melt_dataset(df, id_vars=['date'], val_vars=['sunrise', 'sunset'])
    # Verify the shape of the melted DataFrame
    assert melted_df.shape == (6, 3), f"Expected shape (6, 3), got {melted_df.shape}"
    # Verify the column names
    assert list(melted_df.columns) == ['date', 'symbol', 'times'], f"Expected columns ['date', 'symbol', 'times'], got {list(melted_df.columns)}"
    # Verify the values in the 'symbol' column    
    assert set(melted_df['symbol'].unique()) == {'sunrise', 'sunset'}, f"Expected symbols {{'sunrise', 'sunset'}}, got {set(melted_df['symbol'].unique())}"

    # Test invalid input types
    for invalid_df in [df.to_dict(), df.values, "not a DataFrame", 123]:
        try:
            sun_plts.format.melt_dataset(invalid_df, id_vars=['date'], val_vars=['sunrise', 'sunset'])
            assert False, f"Expected TypeError for non-DataFrame input: {invalid_df}"
        except TypeError as e:
            assert True, f"melt_dataset raised TypeError as expected: {e}"
    for invalid_id_vars in ["date", 123, None, [1,2,3], {}]:
        try:
            sun_plts.format.melt_dataset(df, id_vars=invalid_id_vars, val_vars=['sunrise', 'sunset'])
            assert False, f"Expected TypeError for non-list id_vars: {invalid_id_vars}"
        except TypeError as e:
            assert True, f"melt_dataset raised TypeError as expected: {e}"
    for invalid_val_vars in ["sunrise", 123, None, [1,2,3], {}]:
        try:
            sun_plts.format.melt_dataset(df, id_vars=['date'], val_vars=invalid_val_vars)
            assert False, f"Expected TypeError for non-list val_vars: {invalid_val_vars}"
        except TypeError as e:
            assert True, f"melt_dataset raised TypeError as expected: {e}"

def test_time_of_day():
    """Test the time_of_day function."""
    # Create a sample Series of time objects
    time_series = pd.Series([datetime.time(7, 0), datetime.time(17, 0), pd.NaT])
    # Convert to temporal datetimes
    temporal_series = sun_plts.format.time_of_day(time_series)
    # Verify the type of the output
    assert isinstance(temporal_series, pd.Series), f"Expected output type pd.Series, got {type(temporal_series)}"
    # Verify the values in the output series
    expected_values = [datetime.datetime(2000, 1, 1, 7, 0), datetime.datetime(2000, 1, 1, 17, 0), pd.NaT]
    assert all((temporal_series[i] == expected_values[i]) or (pd.isna(temporal_series[i]) and pd.isna(expected_values[i])) for i in range(len(temporal_series))), f"Expected values {expected_values}, got {list(temporal_series)}"

    # Test invalid input types
    for invalid_series in ["not a Series", 123, None, {}, [1,2,3], [datetime.time(7, 0)]]:
        try:
            sun_plts.format.time_of_day(invalid_series)
            assert False, f"Expected TypeError for non-Series input: {invalid_series}"
        except TypeError as e:
            assert True, f"time_of_day raised TypeError as expected: {e}"
    for invalid_time in ["not a time", 123, {}, datetime.datetime(2000, 1, 1)]:
        try:
            sun_plts.format.time_of_day(pd.Series([invalid_time]))
            assert False, f"Expected TypeError for non-time element in series: {invalid_time}"
        except TypeError as e:
            assert True, f"time_of_day raised TypeError as expected: {e}"