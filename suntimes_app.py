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


st.write("Streamlit supports a wide range of data visualizations, including [Plotly, Altair, and Bokeh charts](https://docs.streamlit.io/develop/api-reference/charts). 📊 And with over 20 input widgets, you can easily make your data interactive!")

possible_data_sets = ["Sunrise", "Sunset", "Daylight"]
with st.container(border=True):
    data_sets = st.multiselect("Data to display:", possible_data_sets, default=possible_data_sets[0:2])
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
