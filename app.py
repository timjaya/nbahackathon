# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from sklearn import datasets
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

iris = datasets.load_iris()
data = pd.DataFrame(data= np.c_[iris['data'], iris['target']],
                     columns= iris['feature_names'] + ['target'])
data.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'target']

conditions = [
    data.target == 0,
    data.target == 1,
    data.target == 2
]
choices = ['setosa','versicolor','virginica']
data.target = np.select(conditions, choices, default='notavailable')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Label('Checkboxes'),
    dcc.Checklist(
        id='checklist',
        options=[
            {'label': 'setosa', 'value': 'setosa'},
            {'label': 'versicolor', 'value': 'versicolor'},
            {'label': 'virginica', 'value': 'virginica'}
        ],
        value=['setosa', 'versicolor', 'virginica']
    ),

    dcc.Graph(
        id='scatter'
    )
])

@app.callback(
    Output('scatter','figure'),
    [Input('checklist','value')]
)
def update_figure(value):
    return {
        'data': [ 
                go.Scatter(
                    x=data[data['target'] == i]['sepal_length'],
                    y=data[data['target'] == i]['sepal_width'],
                    text=data['target'],
                    mode='markers',
                    opacity=0.5,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in value
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
    }

if __name__ == '__main__':
    app.run_server(debug=True)