import json
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State

from Firm import Firm
from utils.logger import get_logger


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

logger = get_logger(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = dbc.Container(html.Div(
                      children=[
                        html.H1(children='The Value Screener'),
                        html.Div(children= (['''
                            Choose a firm to asses
                        ''',
                            html.Br(),
                            dcc.Input(placeholder="Insert the firm's ticker", style={'Align': 'cen'},
                                      id='ticker-input', required=True, type='text'),
                            dcc.Input(placeholder="Insert the firm's market (for US, insert 'us')",
                                      id='market-input', required=True, type='text')])),
                            dbc.Button(
                                        "Generate report",
                                        color="primary",
                                        block=True,
                                        id="button",
                                        className="mb-3",
                                        n_clicks=0
                                    ),
                            dbc.Tabs(
                                        [
                                            dbc.Tab(label="Benjamin Graham", tab_id="Benjamin Graham"),
                                            dbc.Tab(label="Warren Buffet", tab_id="Warren Buffet"),
                                            dbc.Tab(label="Peter Lynch", tab_id="Peter Lynch"),
                                            dbc.Tab(label="James P. O'shaughnessy", tab_id="James P. O'shaughnessy")
                                        ],
                                        id="tabs",
                                        active_tab="Graham"
                                    ),
                          html.Div(id="tab-content", className="p-4"),
                          dcc.Store(id='firm-report')

]
))


@app.callback(
    Output("firm-report", "data"),
    Input("button", "n_clicks"),
    State("ticker-input", "value"),
    State("market-input", "value")

)
def get_full_report(n_clicks, ticker_input, market_input):
    if n_clicks == 0:
        return None
    else:
        firm = Firm(ticker=ticker_input, market=market_input, read_data_dir='data')
        report_df = firm.generate_firm_report()
        json_df = report_df.to_json()
        return json_df


@app.callback(
    Output("tab_content", "children"),
    Input("tabs", "active_tab"),
    State("firm_report", "data")
    )
def render_investor_report(investor, firm_report):
    logger.info(f"Rendering {investor}'s tab")
    if not pd.isnull(investor) and not pd.isnull(firm_report):
        logger.info(f"Fetching {investor}'s report")
        report_json = json.loads(firm_report)
        report_df = pd.DataFrame.from_dict(report_json)
        return dash_table.DataTable(report_df[report_df['investor'] == investor])


if __name__ == '__main__':
    app.run_server()
