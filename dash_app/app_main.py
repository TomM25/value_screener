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
from config import investor_threshold


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
                                        active_tab="Benjamin Graham"
                                    ),
                          html.Div(id="tab-content", className="p-4"),
                          html.Div(id="tab-image", className="p-4", style={'margin': 'auto'}),
                          html.Div(id="tab-summary", className="p-4", style={'margin': 'auto', 'text-align': 'center',
                                                                             'font-size': '30px'}),
                          dcc.Store(id="firm-report")

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
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
    Input("firm-report", "data")
    )
def render_investor_report(investor, firm_report):
    if not pd.isnull(investor) and not pd.isnull(firm_report):
        logger.info(f"Rendering {investor}'s tab")
        logger.info(f"Fetching {investor}'s report")
        report_json = json.loads(firm_report)
        report_df = pd.DataFrame.from_dict(report_json)
        investor_df = report_df[report_df['investor'] == investor]
        investor_df['related_values'] = investor_df['related_values'].astype('str')
        investor_df.drop(columns=['investor', 'test_id', 'investor_test_pass_rate', 'investor_recommendation'],
                         inplace=True)
        investor_df.rename(columns={'description': 'Test description', 'test_passed': 'Test passed?',
                                    'related_values': 'Related values'}, inplace=True)
        return dash_table.DataTable(id="table", columns=[{"name": i, "id": i} for i in investor_df.columns],
                                    data=investor_df.to_dict('records'), style_cell={'text-align': 'left'})


@app.callback(
    Output("tab-summary", "children"),
    Input("tab-content", "children"),
    Input("firm-report", "data"),
    State("tabs", "active_tab")
    )
def summarize_investor_tests(data_table, firm_report, investor):
    if not pd.isnull(data_table) and not pd.isnull(firm_report):
        logger.info(f"Rendering {investor}'s recommendation")
        report_df = pd.DataFrame.from_dict(json.loads(firm_report))
        investor_df = report_df[report_df['investor'] == investor]
        investor_pass_rate = investor_df['investor_test_pass_rate'].values[0]
        investor_thresholds = investor_threshold[investor]
        if investor_pass_rate > investor_thresholds['buy']:
            return html.P([f"Investor tests pass rate: {investor_pass_rate}", html.Br(), f"Investor recommendation: Buy"])

        elif investor_pass_rate > investor_thresholds['hold']:
            return html.P([f"Investor tests pass rate: {investor_pass_rate}", html.Br(), f"Investor recommendation: Hold"])

        else:
            return html.P([f"Investor tests pass rate: {investor_pass_rate}", html.Br(), f"Investor recommendation: Sell"])


@app.callback(
    Output("tab-image", "children"),
    Input("tabs", "active_tab"),
    Input("firm-report", "data")
)
def render_investor_picture(investor, firm_report):
    if not pd.isnull(firm_report):
        investor_pic_path = f"dash_resources//{investor}.png"
        logger.info("Rendering investor image")
        return html.Img(src=investor_pic_path)


if __name__ == '__main__':
    app.run_server(debug=True)
