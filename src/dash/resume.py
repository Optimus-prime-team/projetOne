# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:41:14 2020

@author: utilisateur
"""

import dash
import dash_core_components as dcc
import dash_html_components as html



colors ={
    'background': '#111111',
    'text': '#7FDBFF'
  }




def get_content():
  return html.Div([
     html.H1("GLABAL DATA",
             style={
                     'textAlign': 'center',
                     'color': colors['text']
                     })
  ])