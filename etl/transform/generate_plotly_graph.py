import plotly.graph_objs as go
def generate_plotly_figure(time_samples: list, dict_values: dict, state_dict: dict = {}) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Scatter(x=time_samples, y=value, name=key) for (key, value) in dict_values.items()
        ])
    for key in state_dict.keys():
        fig.add_trace(
            go.Scatter(
                x=time_samples[state_dict.get(key).get("start_time"):state_dict.get(key).get("end_time")],
                y=dict_values["Raw data"][state_dict.get(key).get("start_time"):state_dict.get(key).get("end_time")],
                line=dict(width=1.5),
                fill='tozeroy',
                name=key
            )
        )
    fig.update_xaxes(tickformat="%H:%M:%S")
    return fig