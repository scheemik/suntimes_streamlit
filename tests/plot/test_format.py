import pandas as pd

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