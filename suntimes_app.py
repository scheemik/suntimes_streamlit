import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from suncalc import get_times
from timezonefinder import TimezoneFinderL
tf = TimezoneFinderL(in_memory=True)

# streamlit run suntimes_app.py

from suntimes_streamlit import timezones as tzs
from suntimes_streamlit import time_arrays as tarrs
from suntimes_streamlit import dates as dts

# Insert CSS to have columns exactly fit their content
# From: https://stackoverflow.com/questions/69492406/streamlit-how-to-display-buttons-in-a-single-line
st.markdown("""
        <style>
            div[data-testid="stColumn"] {
                width: fit-content !important;
                flex: unset;
            }
            div[data-testid="stColumn"] * {
                width: fit-content !important;
            }
        </style>
        """, unsafe_allow_html=True)

st.write("Streamlit supports a wide range of data visualizations, including [Plotly, Altair, and Bokeh charts](https://docs.streamlit.io/develop/api-reference/charts). 📊 And with over 20 input widgets, you can easily make your data interactive!")

with st.container(border=True):
    st.title("Select Location")
    st.write("Select a location by latitude and longitude:")
    colA, colB = st.columns([1,1])
    with colA:
        lat = st.number_input("Latitude:", value=43.0, format="%.6f")
    with colB:
        lon = st.number_input("Longitude:", value=-79.0, format="%.6f")
    tz_name, tz_info = tzs.get_tzinfo(lat, lon)
    st.write(f"Timezone: {tz_name}")

with st.container(border=True):
    st.title("Select Time Frame")
    st.write("Select the time frame over which to plot:")
    # Default to starting three months ago and ending nine months from now
    current_date = datetime.now().date()
    three_m_ago = dts.time_math(current_date, months=-3)
    nine_m_from_now = dts.time_math(three_m_ago, years=1)
    select_start = three_m_ago
    select_end = nine_m_from_now
    # Create buttons
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button('Default'):
            select_start = three_m_ago
            select_end = nine_m_from_now
    with col2:
        if st.button('Start today'):
            select_start = current_date
            select_end = dts.time_math(current_date, years=1)
    with col3:
        if st.button('This year'):
            select_start = current_date.replace(month=1, day=1)
            select_end = current_date.replace(month=12, day=31)
    
    # Display the selected times
    colx, coly = st.columns([1,1])
    with colx:
        start_date = st.date_input("Start Date:", select_start)
        st.write(start_date)
    with coly:
        end_date = st.date_input("End Date:", select_end)
        st.write(end_date)
    
    # Toggle UTC
    use_UTC = st.toggle("Use UTC times", value=False)

# Get lists of the possible suncalc attributes and their display names
possible_suncalc_keys = list(tarrs.valid_suncalc_attrs.keys())
possible_suncalc_vals = list(tarrs.valid_suncalc_attrs.values())
# Add "Daylight" as an option
possible_data_vars = possible_suncalc_vals + ["Daylight"]
with st.container(border=True):
    st.title("Select Attributes to Display")
    selected_vars = st.multiselect("Data to display:", possible_data_vars, default=possible_data_vars[2:4])
    take_derivatives = st.toggle("Take derivatives", value=False)

# Get the corresponding keys from the selected display names
selected_keys = []
for var in selected_vars:
    if not var == "Daylight":
        suntime_key = possible_suncalc_keys[possible_suncalc_vals.index(var)]
        selected_keys.append(suntime_key)

# Create the data frame with the selected suntimes
these_times = tarrs.make_suntimes_frame(
    start = start_date,
    end = end_date,
    lat = lat,
    lon = lon,
    suntimes = selected_keys,
)

chart_1_vars = []
chart_2_vars = []
chart_3_vars = []

# Preapare data for plotting
for suntime_key, var in zip(selected_keys, selected_vars):
    if use_UTC:
        these_times[var] = these_times[suntime_key].dt.time
    else:
        these_times[var] = these_times[f"local_{suntime_key}"].dt.time
    chart_1_vars.append(var)
        these_times[set] = these_times[f"local_{suntime_key}"].dt.time
    chart_1_sets.append(set)
# st.write(these_times)
if "Daylight" in selected_vars:
    if not "Sunrise" in chart_1_vars:
        if use_UTC:
            these_times["Sunrise"] = these_times["sunrise"].dt.time
        else:
            these_times["Sunrise"] = these_times[f"local_sunrise"].dt.time
    if not "Sunset" in chart_1_vars:
        if use_UTC:
            these_times["Sunset"] = these_times["sunset"].dt.time
        else:
            these_times["Sunset"] = these_times[f"local_sunset"].dt.time
    these_times["Daylight"] = pd.to_timedelta(these_times["sunset"] - these_times["sunrise"])
    chart_2_vars.append("Daylight")
    st.write(these_times["Daylight"].values[0])

if take_derivatives:
    for var in selected_vars:
        d_var = rf'{var} change'
        st.write(f"{d_var}")
        if not var == "Daylight":
            chart_3_vars.append(d_var)
            data[f"n_min_{var}"] = (data[var] - np.datetime64(test_date)).dt.total_seconds() / 60
            data[d_var] = data[f"n_min_{var}"].diff()

# st.write(f"chart_1_vars: {chart_1_vars}")
# st.write(f"chart_2_vars: {chart_2_vars}")
# st.write(f"chart_3_vars: {chart_3_vars}")

# Look at this site for mouse-over tools:
# https://docs.streamlit.io/develop/tutorials/elements/annotate-an-altair-chart

tab1, tab2, tab3 = st.tabs(["Chart", "Dataframe", "Testing"])
if len(chart_1_vars) > 0:
    chart_1_vars.append('date')
    # tab1.line_chart(these_times[chart_1_vars], x='date', x_label="Date", y_label=f"Time", height=250)
    # Create an Altair line chart with the selected vars, and with mouse-over tooltips showing the date and time values
    # Melt the dataframe so that there is a "symbol" column with the var name, and a "value" column with the time value
    chart_1_vars_melted = these_times.melt(id_vars=['date'], value_vars=chart_1_vars[:-1], var_name='symbol', value_name='times')
    # Convert time objects (including tz-aware times) to temporal datetimes for charting.
    chart_1_sets_melted['times_temporal'] = chart_1_sets_melted['times'].apply(
        lambda t: pd.NaT if pd.isna(t) else datetime.combine(datetime(2000, 1, 1), t.replace(tzinfo=None))
    )
    hover = alt.selection_point(
        fields=['date'],
        nearest=True,
        on='mouseover',
        empty='none',
    )
    lines = (
        alt.Chart(chart_1_vars_melted, title="Suntimes")
        .mark_line()
        .encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('times_temporal:T', title='Time of Day', axis=alt.Axis(format='%H:%M')),
            color=alt.Color('symbol', title='Suntime'),
        )
    )
    points = lines.transform_filter(hover).mark_circle(size=65)
    tooltips = alt.Chart(chart_1_vars_melted).mark_rule().encode(
        x='date:T',
        opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
        tooltip=[
            # Format the date in the tooltip to be DD MMM YYYY
            alt.Tooltip('date:T', title='Date', format='%d %b %Y'),
            alt.Tooltip('symbol:N', title='Suntime'),
            alt.Tooltip('times_temporal:T', title='Time', format='%H:%M'),
        ]
    ).add_params(hover)
    chart = lines + points + tooltips
    tab1.altair_chart(chart, use_container_width=True)

if len(chart_2_vars) > 0:
    chart_2_vars.append('date')
    tab1.line_chart(these_times[chart_2_vars], x='date', x_label="Date", y_label=f"Time", height=250)
if len(chart_3_vars) > 0:
    chart_3_vars.append('date')
    tab1.line_chart(these_times[chart_3_vars], x='date', x_label="Date", y_label=f"Change (minutes / day)", height=250)
tab2.dataframe(these_times, height=250, width="stretch")
tab2.dataframe(chart_1_vars_melted, height=250, width="stretch")