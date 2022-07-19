from dash import Dash, dcc, html, Input, Output, callback_context
from main_handler import extract, transform, load
import numpy as np
from typing import Union



div_style = {"alignSelf": "center", "justifyContent": "center", "textAlign": "center", "alignItems": "center", "position": "center", "width": "50%", "margin": "0 auto", "marginBottom": "1em"}
restart_style = {"alignSelf": "center", "justifyContent": "center", "textAlign": "center", "alignItems": "center","maxWidth": "12em", "position": "center", "width": "50%", "margin": "0 auto", "marginTop": "1em", "marginBottom": "1em", "color": "blue"}
dropdown_style = {"alignSelf": "center", "justifyContent": "center", "textAlign": "center", "alignItems": "center","maxWidth": "24em", "position": "center", "width": "50%", "margin": "0 auto"}
dropdown_style = {"display": "block", "width": "50%", "margin": "0 auto", "marginBottom": "2em"}
tables_checklist_style = {"display": "block", "width": "50%", "margin": "0 auto", "marginBottom": "2em"}
hide_elem = {"display": "none"}
graph_style = {"display": "block"}


app = Dash("dash.app", title="NILM Project")
app.layout = html.Div(children=[
    html.H1(children='NILM Dashboard control', style={"textAlign": "center"}),
    html.H3(children='Initial extracted data, select a mode to operate on:',
        style={"textAlign": "center"}
    ),
    html.Div(children=[
        html.Button('Train ML',
            id='train_model',
            n_clicks=0),
        html.Button('Predict ML',
            id='predict_model',
            n_clicks=0),
    ], style=div_style),

    html.Button('Restart', id='restart', style=restart_style,
        n_clicks=0),

    dcc.Dropdown(
        extract.get_database(), id="dbs_dropdown",style=hide_elem
    ),
    dcc.Dropdown(
        [], id="table_checklist", style=hide_elem
    ),

    dcc.Graph(
        figure={},
        id="param_specific_plot",
        style=hide_elem
    )
])
@app.callback(
    Output('dbs_dropdown', 'style'),
    Output('train_model', 'disabled'),
    Output('predict_model', 'disabled'),
    Output('restart', 'disabled'),
    Input('train_model', 'n_clicks'),
    Input('predict_model', 'n_clicks'),
    Input('restart', 'n_clicks')
)
def displayClick(_train_model_btn, _predict_model_btn, _restart_btn):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'train_model' in changed_id:
        return dropdown_style, False, True, False
    elif 'predict_model' in changed_id:
        return dropdown_style, True, False, False
    elif 'restart' in changed_id:
        return hide_elem, False, False, True
    else:
        return hide_elem, False, False, True

@app.callback(
    Output('table_checklist', 'options'),
    Output('table_checklist', 'style'),
    Input('dbs_dropdown', 'style'),
    Input('dbs_dropdown', 'value')
)
def get_tables(style_dict: dict, db: str) -> Union[list, dict]:
    if style_dict.get("display") == "block" and db:
        return extract.get_table(db), tables_checklist_style
    return [], hide_elem


@app.callback(
    Output('param_specific_plot', 'style'),
    Output('param_specific_plot', 'figure'),
    Input('dbs_dropdown', 'value'),
    Input('table_checklist', 'value')
)
def update_graph(db: str, table: str):
    if db and table:
        filename= extract.get_filename(db, table)
        try:
            df = transform.clean_df(extract.extract_pandas(filename))
        except:
            df = transform.clean_df(extract.extract_pandas(filename, sep_attempt=","))

        print(df, flush=True)

        BASE_ZERO_DATA_LIST = transform.convert_date_samples(df.StringTime)
        ARRAY_FILTERED = transform.clean_noise(np.gradient(transform.clean_noise(df["I3"], 31, 2), edge_order=2), 5, 3)

        load.generate_state(
        _array=ARRAY_FILTERED
        )

        return graph_style, transform.generate_figure(
            BASE_ZERO_DATA_LIST,
            {
                "Raw data": df["I3"],
                "Filtered data": transform.clean_noise(df["I3"]),
            },
            extract.get_state(load.STATE_FILE_PATH)
            )
    return hide_elem, {}


app.run_server(debug=True)
