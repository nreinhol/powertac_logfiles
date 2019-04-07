import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import flask
import pandas as pd
import os

import ewiis3DatabaseConnector as db

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

df_order_submits = db.load_order_submits()
df_cleared_trades = db.load_full_table_cleared_trades()
df_order_submits['proximity'] = df_order_submits['targetTimeslot'] - df_order_submits['timeslotIndex']

"""df_tariff_subscriptions = db.load_tariff_transactions()
df_tariff_subscriptions = df_tariff_subscriptions[df_tariff_subscriptions['txType'].isin(['CONSUME', 'PRODUCE'])]
df_tariff_subscriptions_grouped = df_tariff_subscriptions[
        ['currentSubscribedPopulation', 'currentSubscribedPopulationShareOnPowerType', 'gameId', 'customerName', 'postedTimeslotIndex', 'txType',
         'powerType']].groupby(by=['postedTimeslotIndex', 'powerType', 'gameId'], as_index=False).sum()"""

df_tariff_subscriptions_shares = db.load_tariff_subscription_shares()

df_tariff_subscriptions_shares = df_tariff_subscriptions_shares.melt(
    id_vars=['tariffSubscriptionId', 'gameId', 'timeslotIndex'], var_name='powerType')

df_all_offered_tariffs = db.load_tariff_specification_meets_avg_rates()

options = []

for proximity in list(df_order_submits['proximity'].unique()):
    options.append({'label': proximity, 'value': proximity})

app = dash.Dash('app', server=server)
app.config.suppress_callback_exceptions = True

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'


####################################################
#### Tariff Page
####################################################


def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


tariff_page = html.Div([
    dcc.Link('Go to Wholesale Market', href='/page-2'),
    dcc.Link('Go to Customer Analysis', href='/page-3'),
    html.Br(),
    dcc.Dropdown(
        id='dropdown-game-id',
        options=[{'label': i, 'value': i} for i in df_tariff_subscriptions_shares['gameId'].unique()],
        value=df_tariff_subscriptions_shares['gameId'].values[0]
    ),
    html.H1('Tariff market share'),
    dcc.Graph(id='tariff-share'),
    html.H1('All offered tariffs'),
    generate_table(df_all_offered_tariffs[
                       ["brokerName", "earlyWithdrawPayment", "minDuration", "periodicPayment", "postedTimeslotIndex",
                        "powerType", "signupPayment", "AVG(minValueMoney)", "AVG(maxValueMoney)", "AVG(maxCurtailment)",
                        "AVG(tierThreshold)", "AVG(downRegulationPayment)", "AVG(upRegulationPayment)", "rateCount"]])
], className="container")


@app.callback(Output('tariff-share', 'figure'),
              [Input('dropdown-game-id', 'value')])
def update_graph_tariff_share(game_id_value):
    dff = df_tariff_subscriptions_shares[df_tariff_subscriptions_shares['gameId'] == game_id_value]
    # dff = dff[dff['proximity'] == proximity_value]
    # dff = df_order_submits[df_order_submits['proximity'] == proximity_value]

    return {
        'data': [
            go.Scatter(
                x=dff[dff['powerType'] == i]['timeslotIndex'],
                y=dff[dff['powerType'] == i]['value'],
                # text=str(df_order_submits[df_order_submits['proximity'] == i]['proximity']),
                mode='lines',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in dff.powerType.unique()
        ],
        'layout': go.Layout(
            xaxis={'type': 'linear', 'title': 'mktPrice'},
            yaxis={'title': 'mktQty'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


####################################################
#### Routing
####################################################

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return tariff_page
    elif pathname == '/page-2':
        return wholesale_page
    elif pathname == '/page-3':
        return customer_page
    else:
        return tariff_page
        # You could also return a 404 "URL not found" page here


####################################################
#### Wholesale Market
####################################################


wholesale_page = html.Div([
    dcc.Link('Go to Tariff Market', href='/page-1'),
    dcc.Link('Go to Customer Analysis', href='/page-3'),
    html.Br(),
    dcc.Dropdown(
        id='dropdown-game-id',
        options=[{'label': i, 'value': i} for i in df_tariff_subscriptions_shares['gameId'].unique()],
        value=df_tariff_subscriptions_shares['gameId'].values[0]
    ),
    dcc.Dropdown(
        id='dropdown-proximity',
        options=[{'label': i, 'value': i} for i in df_order_submits['proximity'].unique()],
        value=1
    ),
    html.H1('Wholesale Market'),
    dcc.Graph(id='wholesale-quantities'),
    dcc.Graph(id='wholesale-orders'),
    dcc.Graph(id='cleared-trades')
], className="container")


@app.callback(Output('wholesale-quantities', 'figure'),
              [Input('dropdown-proximity', 'value'), Input('dropdown-game-id', 'value')])
def update_graph_wholesale_quantities(proximity_value, game_id_value):
    dff = df_order_submits[df_order_submits['gameId'] == game_id_value]
    dff = dff[dff['proximity'] == proximity_value]
    # dff = df_order_submits[df_order_submits['proximity'] == proximity_value]

    return {
        'data': [{
            'x': dff.targetTimeslot,
            'y': dff.clearedMWh,
            'name': 'clearedMWh',
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }, {
            'x': dff.targetTimeslot,
            'y': dff.orderMWh,
            'name': 'orderMWh',
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }],
        'layout': {
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            }
        }
    }


@app.callback(Output('wholesale-orders', 'figure'),
              [Input('dropdown-proximity', 'value'), Input('dropdown-game-id', 'value')])
def update_graph_wholesale_orders(proximity_value, game_id_value):
    dff = df_order_submits[df_order_submits['gameId'] == game_id_value]
    # dff = dff[dff['proximity'] == proximity_value]
    # dff = df_order_submits[df_order_submits['proximity'] == proximity_value]

    return {
        'data': [
            go.Scatter(
                y=dff[dff['proximity'] == i]['limitPrice'],
                x=dff[dff['proximity'] == i]['orderMWh'],
                # text=str(df_order_submits[df_order_submits['proximity'] == i]['proximity']),
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=str(i)
            ) for i in dff.proximity.unique()
        ],
        'layout': go.Layout(
            xaxis={'type': 'linear', 'title': 'mktPrice'},
            yaxis={'title': 'mktQty'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


@app.callback(Output('cleared-trades', 'figure'),
              [Input('dropdown-proximity', 'value'), Input('dropdown-game-id', 'value')])
def update_graph_cleared_trades(proximity_value, game_id_value):
    dff = df_cleared_trades[df_cleared_trades['gameId'] == game_id_value]
    # dff = dff[dff['proximity'] == proximity_value]
    # dff = df_order_submits[df_order_submits['proximity'] == proximity_value]

    return {
        'data': [
            go.Scatter(
                x=dff['executionPrice'],
                y=dff['executionMWh'],
                # text=str(df_order_submits[df_order_submits['proximity'] == i]['proximity']),
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )
        ],
        'layout': go.Layout(
            xaxis={'type': 'linear', 'title': 'mktPrice'},
            yaxis={'title': 'mktQty'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


df_tariff_transactions = db.load_tariff_transactions()
allow = ['PRODUCE', 'CONSUME']
df_tariff_transactions_prod_con = df_tariff_transactions[df_tariff_transactions['txType'].isin(allow)]

# df['kWh_per_customer'] = df['kWh'] / df['currentSubscribedPopulation']
# df_tariff_transactions_prod_con['kWhPerCustomer'] = df_tariff_transactions_prod_con['kWh'] / df_tariff_transactions_prod_con['currentSubscribedPopulation']
# df_customer = df_tariff_transactions_prod_con[['kWhPerCustomer', 'customerName', 'postedTimeslotIndex', 'gameId']].groupby(by=['postedTimeslotIndex', 'customerName', 'gameId'], as_index=False).sum()
df_customer = df_tariff_transactions_prod_con[['kWh', 'customerName', 'postedTimeslotIndex', 'gameId']].groupby(
    by=['postedTimeslotIndex', 'customerName', 'gameId'], as_index=False).sum()

df_all = df_tariff_transactions_prod_con[['kWh', 'postedTimeslotIndex', 'gameId']].groupby(
    by=['postedTimeslotIndex', 'gameId'], as_index=False).sum()

options = [{'label': 'all', 'value': 'all'}]

for customer in list(df_customer['customerName'].unique()):
    options.append({'label': customer, 'value': customer})

####################################################
#### Customer Page
####################################################

customer_page = html.Div([
    dcc.Link('Go to Tariff Market', href='/page-1'),
    dcc.Link('Go to Wholesale Market', href='/page-2'),
    html.H1('Power Type'),
    dcc.Dropdown(
        id='game_id',
        options=[{'label': i, 'value': i} for i in list(df_customer['gameId'].unique())],
        value=list(df_customer['gameId'].unique())[0]
    ),
    dcc.Dropdown(
        id='proximity',
        options=[{'label': i, 'value': i} for i in df_order_submits['proximity'].unique()],
        value=1
    ),
    dcc.Dropdown(
        id='customer_selection',
        options=options,
        value='all'
    ),
    dcc.Graph(id='customer_prosumption'),
    dcc.Graph(id='imbalance'),
    dcc.Graph(id="customer_prosumption-imbalance")
], className="container")


@app.callback(Output('customer_prosumption', 'figure'),
              [Input('customer_selection', 'value'), Input('game_id', 'value'), Input('proximity', 'value')])
def update_graph(selected_dropdown_value, game_id, proximity):
    df_customer_prosumption_prediction = db.load_predictions('prediction', game_id, 'customer', 'prosumption')
    df_customer_prosumption_prediction = df_customer_prosumption_prediction[
        df_customer_prosumption_prediction['proximity'] == proximity]

    if selected_dropdown_value == 'all':
        dff = df_all[df_all['gameId'] == game_id]
    else:
        dff = df_customer[df_customer['gameId'] == game_id]
        dff = dff[dff['customerName'] == selected_dropdown_value]

    return {
        'data': [{
            'x': dff.postedTimeslotIndex,
            'y': dff.kWh,
            'line': {
                'width': 3,
                'shape': 'spline'
            },
            'name': 'customerProsumption'
        }, {
            'x': df_customer_prosumption_prediction.target_timeslot,
            'y': df_customer_prosumption_prediction.prediction,
            'line': {
                'width': 3,
                'shape': 'spline'
            },
            'name': 'customerProsumptionPred'
        }],
        'layout': {
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            }
        }
    }


@app.callback(Output('imbalance', 'figure'),
              [Input('customer_selection', 'value'), Input('game_id', 'value'), Input('proximity', 'value')])
def update_graph(selected_dropdown_value, game_id, proximity):
    df_grid_imbalance_pred = db.load_predictions('prediction', game_id, 'grid', 'imbalance')
    df_grid_imbalance_pred = df_grid_imbalance_pred[df_grid_imbalance_pred['proximity'] == proximity]
    df_grid_imbalance = db.load_balance_report(game_id)

    return {
        'data': [{
            'x': df_grid_imbalance_pred.target_timeslot,
            'y': df_grid_imbalance_pred.prediction,
            'line': {
                'width': 3,
                'shape': 'spline'
            },
            'name': 'gridImbalancePred'
        }, {
            'x': df_grid_imbalance.timeslotIndex,
            'y': df_grid_imbalance.netImbalance,
            'line': {
                'width': 3,
                'shape': 'spline'
            },
            'name': 'gridImbalancePred'
        }],
        'layout': {
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            }
        }
    }


@app.callback(Output('customer_prosumption-imbalance', 'figure'),
              [Input('customer_selection', 'value'), Input('game_id', 'value'), Input('proximity', 'value')])
def update_graph(selected_dropdown_value, game_id, proximity):
    df_grid_imbalance_pred = db.load_predictions('prediction', game_id, 'grid', 'imbalance')
    df_grid_imbalance_pred = df_grid_imbalance_pred[df_grid_imbalance_pred['proximity'] == proximity]
    df_grid_imbalance_pred.rename(columns={'prediction': 'imb_prediction'}, inplace=True)
    df_grid_imbalance_pred['strategic_imbalance'] = df_grid_imbalance_pred['imb_prediction'] * -1

    df_customer_prosumption_prediction = db.load_predictions('prediction', game_id, 'customer', 'prosumption')
    df_customer_prosumption_prediction = df_customer_prosumption_prediction[
        df_customer_prosumption_prediction['proximity'] == proximity]
    df_customer_prosumption_prediction.rename(columns={'prediction': 'cpros_prediction'}, inplace=True)

    df_imb_and_prosumption = df_grid_imbalance_pred.merge(df_customer_prosumption_prediction, how='left',
                                                          on='target_timeslot')
    df_imb_and_prosumption['wholesalebid'] = -df_imb_and_prosumption['cpros_prediction'] + df_imb_and_prosumption[
                                                                                               'imb_prediction'] * 0.3
    df_imb_and_prosumption = df_imb_and_prosumption[
        ['target_timeslot', 'cpros_prediction', 'imb_prediction', 'wholesalebid']]
    print(df_grid_imbalance_pred.head())
    print(df_customer_prosumption_prediction.head())
    print(df_imb_and_prosumption[df_imb_and_prosumption['target_timeslot'] > 962].head())

    df_EWIIS3_imbalance = db.load_balancing_transactions()
    df_EWIIS3_imbalance = df_EWIIS3_imbalance[df_EWIIS3_imbalance["gameId"] == game_id]

    df_grid_imbalance = db.load_balance_report()
    df_grid_imbalance = df_grid_imbalance[df_grid_imbalance["gameId"] == game_id]

    return {
        'data': [{
            'x': df_imb_and_prosumption.target_timeslot,
            'y': df_imb_and_prosumption.wholesalebid,
            'line': {
                'width': 3,
                'shape': 'spline'
            },
            'name': 'wholesalebid'
        }, {
            'x': df_grid_imbalance_pred.target_timeslot,
            'y': df_grid_imbalance_pred.strategic_imbalance,
            'line': {
                'width': 3,
                'shape': 'spline'
            },
            'name': 'strategic_imbalance'
        }, {
            'x': df_EWIIS3_imbalance.postedTimeslot,
            'y': df_EWIIS3_imbalance.kWh,
            'line': {
                'width': 3,
                'shape': 'spline'
            },
            'name': 'EWIIS3Imbalance'
        }, {
            'x': df_grid_imbalance.timeslotIndex,
            'y': df_grid_imbalance.netImbalance,
            'line': {
                'width': 3,
                'shape': 'spline'
            },
            'name': 'gridImbalance'
        }],
        'layout': {
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            }
        }
    }


if __name__ == '__main__':
    app.run_server()
