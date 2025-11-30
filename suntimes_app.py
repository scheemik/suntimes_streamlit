import streamlit as st
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
    st.title("Location")
    st.write("Select a location by latitude and longitude:")
    colA, colB = st.columns([1,1])
    with colA:
        lat = st.number_input("Latitude:", value=43.0, format="%.6f")
    with colB:
        lon = st.number_input("Longitude:", value=-79.0, format="%.6f")
    tz_name, tz_info = tzs.get_tzinfo(lat, lon)
    st.write(f"Timezone: {tz_name}")#, tz_info: {type(tz_info)}")

    st.title("Time frame")
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

possible_suncalc_keys = list(tarrs.valid_suncalc_attrs.keys())
possible_suncalc_vals = list(tarrs.valid_suncalc_attrs.values())
possible_data_sets = possible_suncalc_vals + ["Daylight"]
with st.container(border=True):
    data_sets = st.multiselect("Data to display:", possible_data_sets, default=possible_data_sets[2:4])
    take_derivatives = st.toggle("Take derivatives")

these_times = tarrs.make_suntimes_frame(
    start = start_date,
    end = end_date,
    lat = lat,
    lon = lon,
    suntimes = [ds.lower() for ds in data_sets if not ds == "Daylight"],
)

# st.write(these_times.columns)
# st.write(these_times)

chart_1_sets = []
chart_2_sets = []
chart_3_sets = []
if "Sunrise" in data_sets or "Daylight" in data_sets:
    chart_1_sets.append("Sunrise")
    # Remove the date to get just the time
    these_times["Sunrise"] = these_times["local_sunrise"].dt.time
if "Sunset" in data_sets or "Daylight" in data_sets:
    chart_1_sets.append("Sunset")
    # Remove the date to get just the time
    these_times["Sunset"] = these_times["local_sunset"].dt.time
if "Daylight" in data_sets:
    chart_2_sets.append("Daylight")
    these_times["Daylight"] = pd.to_timedelta(these_times["Sunset"] - these_times["Sunrise"])

if take_derivatives:
    for set in data_sets:
        d_set = rf'{set} change'
        st.write(f"{d_set}")
        if not set == "Daylight":
            chart_3_sets.append(d_set)
            data[f"n_min_{set}"] = (data[set] - np.datetime64(test_date)).dt.total_seconds() / 60
            data[d_set] = data[f"n_min_{set}"].diff()

# st.write(f"chart_1_sets: {chart_1_sets}")
# st.write(f"chart_2_sets: {chart_2_sets}")
# st.write(f"chart_3_sets: {chart_3_sets}")

# Look at this site for mouse-over tools:
# https://docs.streamlit.io/develop/tutorials/elements/annotate-an-altair-chart

tab1, tab2, tab3 = st.tabs(["Chart", "Dataframe", "Testing"])
if len(chart_1_sets) > 0:
    chart_1_sets.append('date')
    tab1.line_chart(these_times[chart_1_sets], x='date', x_label="Date", y_label=f"Time", height=250)
if len(chart_2_sets) > 0:
    chart_2_sets.append('date')
    tab1.line_chart(these_times[chart_2_sets], x='date', x_label="Date", y_label=f"Time", height=250)
if len(chart_3_sets) > 0:
    chart_3_sets.append('date')
    tab1.line_chart(these_times[chart_3_sets], x='date', x_label="Date", y_label=f"Change (minutes / day)", height=250)
tab2.dataframe(these_times, height=250, width="stretch")
