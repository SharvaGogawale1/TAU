from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
# import plotly.graph_objs as go
import numpy as np
import os

import plotly.graph_objs as go
def generate_plotly_figure(time_samples: list, dict_values: dict) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Scatter(x=time_samples, y=value, name=key) for (key, value) in dict_values.items()
        ])
    fig.add_trace(go.Scatter(
    x=BASE_ZERO_DATA_LIST[50:1000], y=np.ones(950),
    stackgroup='one',
    mode='lines',
    line=dict(width=1.5, color='rgb(111, 231, 219)'),
    name="Stage1"
    ))
    fig.update_xaxes(tickformat="%H~%M~%S")
    return fig

from datetime import datetime
from scipy.signal import savgol_filter

def features_extraction_mock(df: pd.DataFrame) -> dict:
    try:
        df.drop(columns="DoubleTime", inplace=True)
        df.drop(index=0, inplace=True)
        df["StringTime"] = [datetime.strptime(time[:time.find(".")], '%m/%d/%y  %H:%M:%S') for time in df["StringTime"]]
        df["StringTime"] = df.StringTime - df.StringTime.iloc[0] # setting base 0 for time comparission
    except:
        raise Exception("Error")
    return df

def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%02d:%02d:%02d" % (hour, min, sec)

app = Dash("dash.app", title="NILM Project")

extracted_data = pd.read_csv(os.path.join(os.getcwd(), 'data', 'data_new.csv'))
data = features_extraction_mock(extracted_data)

BASE_ZERO_DATA_LIST = [date_sample[date_sample.rfind(" ")+len(" "):] for date_sample in data.StringTime.apply(str)]

# def generate_plotly_figure(param_to_plot: str) -> go.Figure:
#     fig = go.Figure(
#         data=[
#             go.Scatter(x=BASE_ZERO_DATA_LIST, y=data[param_to_plot], name="Raw data"),
#             # go.Scatter(x=BASE_ZERO_DATA_LIST, y=np.gradient(data[param_to_plot])),
#             # go.Scatter(x=BASE_ZERO_DATA_LIST, y=20*np.log(abs(np.fft.fft(data[param_to_plot])))),
#             go.Scatter(x=BASE_ZERO_DATA_LIST, y=savgol_filter(data[param_to_plot], 19, 2), name="Filtered data"),
#             # go.Scatter(x=BASE_ZERO_DATA_LIST, y=savgol_filter(np.gradient(data[param_to_plot]), 19, 2)),
#             # go.Scatter(x=BASE_ZERO_DATA_LIST, y=20*np.log(abs(np.fft.fft(savgol_filter(data[param_to_plot], 11, 3))))),
#         ])
#     fig.update_xaxes(tickformat="%H~%M~%S")
#     return fig



fig = generate_plotly_figure(
    BASE_ZERO_DATA_LIST,
    {
        "Raw data": data["I3"],
        "Filtered data": savgol_filter(data["I3"], 19, 2),
        "Gradient": np.gradient(savgol_filter(data["I3"], 19, 2))
    })



app.layout = html.Div(children=[
    html.H1(children='NILM Dashboard control'),
    # dcc.Graph(figure=impedance_fig,id='impedence'),
    html.Div(children='''
        Initial extracted data, select an extracted parameters to visualize
    '''),
    dcc.Dropdown(data.columns, "I3", id='param_to_plot'),
    dcc.Graph(
        figure=fig,
        id="param_specific_plot"
    )

])
@app.callback(
    Output('param_specific_plot', 'figure'),
    Input('param_to_plot', 'value')
)
def update_graph(value):
    return generate_plotly_figure(
        BASE_ZERO_DATA_LIST,
        {
            "Raw data": data[value],
            "Filtered data": savgol_filter(data[value], 19, 2),
            "Gradient": np.gradient(savgol_filter(data[value], 19, 2))
        })

app.run_server(debug=True)
