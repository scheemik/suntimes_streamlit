import streamlit as st
import pandas as pd
import numpy as np

def make_sin_wave(
    x_arr,
    freq=1,
    amp=1,
    phase_shift=0,
    vert_shift=0,
):
    y_arr = amp * np.sin(2*np.pi * (x_arr - phase_shift) / freq) + amp
    y_arr = pd.to_timedelta(y_arr, unit="minutes") + vert_shift
    return y_arr

st.write("Streamlit supports a wide range of data visualizations, including [Plotly, Altair, and Bokeh charts](https://docs.streamlit.io/develop/api-reference/charts). 📊 And with over 20 input widgets, you can easily make your data interactive!")

possible_data_sets = ["Sunrise", "Sunset", "Daylight"]
with st.container(border=True):
    data_sets = st.multiselect("Data to display:", possible_data_sets, default=possible_data_sets[0:2])
    take_derivatives = st.toggle("Take derivatives")

data = pd.DataFrame({'date':pd.date_range(start='2020-01-01', end='2020-12-31')})

data_len = len(data)
x_data = np.arange(data_len)
test_date = '2020-01-01'

st.write(f"Type of 'date' data: {type(data.date.values[0])}")
st.write(f"{np.datetime64(f'{test_date} 06:00')}")

chart_1_sets = []
chart_2_sets = []
chart_3_sets = []
if "Sunrise" in data_sets or "Daylight" in data_sets:
    chart_1_sets.append("Sunrise")
    this_time = np.datetime64(f'{test_date} 06:00')
    data["Sunrise"] = make_sin_wave(x_data, amp=120, freq=data_len, vert_shift=this_time)
if "Sunset" in data_sets or "Daylight" in data_sets:
    chart_1_sets.append("Sunset")
    this_time = np.datetime64(f'{test_date} 18:00')
    data["Sunset"] = make_sin_wave(x_data, amp=60, freq=data_len, vert_shift=this_time, phase_shift=30)
if "Daylight" in data_sets:
    chart_2_sets.append("Daylight")
    data["Daylight"] = pd.to_timedelta(data["Sunset"] - data["Sunrise"])

if take_derivatives:
    for set in data_sets:
        d_set = rf'{set} change'
        st.write(f"{d_set}")
        if not set == "Daylight":
            chart_3_sets.append(d_set)
            data[f"n_min_{set}"] = (data[set] - np.datetime64(test_date)).dt.total_seconds() / 60
            data[d_set] = data[f"n_min_{set}"].diff()

st.write(f"chart_1_sets: {chart_1_sets}")
st.write(f"chart_2_sets: {chart_2_sets}")
st.write(f"chart_3_sets: {chart_3_sets}")

tab1, tab2 = st.tabs(["Chart", "Dataframe"])
if len(chart_1_sets) > 0:
    chart_1_sets.append('date')
    tab1.line_chart(data[chart_1_sets], x='date', x_label="Date", y_label=f"Time", height=250)
if len(chart_2_sets) > 0:
    chart_2_sets.append('date')
    tab1.line_chart(data[chart_2_sets], x='date', x_label="Date", y_label=f"Time", height=250)
if len(chart_3_sets) > 0:
    chart_3_sets.append('date')
    tab1.line_chart(data[chart_3_sets], x='date', x_label="Date", y_label=f"Change (minutes / day)", height=250)
tab2.dataframe(data, height=250, width=True)