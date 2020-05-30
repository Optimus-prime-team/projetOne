# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:02:48 2020

@author: utilisateur
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import resume as resume
import paris as paris
import lyon as lyon
import toulouse as toulouse
import nantes as nantes
import bordeaux as bordeaux



colors ={
    'background': '#111111',
    'text': '#7FDBFF'
  }

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children="Job's Statistics in 5 French Town, for 5 carriers in Data and IT",
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    dcc.Tabs(id="tabs", value='resume', children=[
        dcc.Tab(label='Global data', value='resume'),
        dcc.Tab(label='Paris data', value='paris'),
        dcc.Tab(label='Lyon data', value='lyon'),
        dcc.Tab(label='Toulouse Data', value='toulouse'),
        dcc.Tab(label='Nantes Data', value='nantes'),
        dcc.Tab(label='Bordeaux Data', value='bordeaux'),
    ]),
    html.Div(id='tabs-content'),

])


#@app.callback(Output('live-update-text', 'children'),
#              [Input('interval-component', 'n_intervals')])
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    print(tab)
    if tab == 'resume':
        return resume.get_content()
    elif tab == 'paris':
        return paris.get_content()
    elif tab == 'lyon':
        return lyon.get_content()
    elif tab == 'toulouse' :
        return toulouse.get_content()
    elif tab == 'nantes':
        return nantes.get_content()
    elif tab == 'bordeaux' :
        return bordeaux.get_content()

if __name__ == '__main__':
    #app.run_server(debug=False)
    app.run_server(debug=True, use_reloader=False)
