import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask
import pandas as pd
import time
import os

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

df = pd.read_csv('totalCustomerProdCon.csv')
allow = ['PRODUCE', 'CONSUME']
df = df[df['txType'].isin(allow)]

# df['kWh_per_customer'] = df['kWh'] / df['currentSubscribedPopulation']
df['kWhPerCustomer'] = df['kWh'] / df['currentSubscribedPopulation']
df_customer = df[['kWhPerCustomer', 'customerName', 'postedTimeslotIndex']].groupby(by=['postedTimeslotIndex', 'customerName'], as_index=False).sum()

df_all = df[['kWh', 'postedTimeslotIndex']].groupby(by=['postedTimeslotIndex'], as_index=False).sum()

options = [{'label': 'all', 'value': 'all'}]

for customer in list(df_customer['customerName'].unique()):
    options.append({'label': customer, 'value': customer})

app = dash.Dash('app', server=server)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Power Type'),
    dcc.Dropdown(
        id='my-dropdown',
        options=options,
        value='all'
    ),
    dcc.Graph(id='my-graph')
], className="container")

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])

def update_graph(selected_dropdown_value):
    if selected_dropdown_value == 'all':
        dff = df_all
    else:
        dff = df_customer[df_customer['customerName'] == selected_dropdown_value]

    return {
        'data': [{
            'x': dff.postedTimeslotIndex,
            'y': dff.kWhPerCustomer,
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

if __name__ == '__main__':
    app.run_server()
