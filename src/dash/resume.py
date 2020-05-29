# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:41:14 2020

@author: utilisateur
"""
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import sys
sys.path.append('../indeed/')
import mongo_indeed as bdd
import numpy as np
colors ={
    'background': '#111111',
    'text': '#7FDBFF'
  }

df =  bdd.load_offers()

# data Cleaning
df.drop(index = df[df['city_querry'].isnull()].index, inplace = True)

# convert 0.0 to nan
df['salary'] = df['salary'].replace(0, np.nan)

# mise en place du titre
title ="Nombre d'offre scrappées : "+str(len(df))

# données pour le pie % d'offre par ville
labels_city = df.city_querry.unique().tolist()
values = []
for elt in labels_city :
    values.append(len(df[df['city_querry'] == elt]))
data_city = [
    {
        'values': values,
        'type': 'pie',
        'labels' : labels_city,       
        },
    ]


# données pour le pie % d'offre par type d'emploi
labels_job = df.job_querry.unique().tolist()
nbr_job = []
for elt in labels_job :
    nbr_job.append(len(df[df['job_querry'] == elt]))
data_job = [
        {
        'values': nbr_job,
        'type': 'pie',
        'labels' : labels_job,       
        },  
     ]
# données pour le pie % d'offre avec salaire
labels_salaire = ['avec salaire', 'sans salaire']
df_avec_salaire = df[df['salary'] > 0]

nbr_salaire = [len(df_avec_salaire), (len(df) - len(df_avec_salaire))]

data_salaire = [
        {
        'values': nbr_salaire,
        'type': 'pie',
        'labels' : labels_salaire,       
        },  
     ]







def get_content():
  return html.Div([
     html.H1("GLABAL DATA",
             style={
                     'textAlign': 'center',
                     'color': colors['text']
                     }),
    html.H2(title,
             style={
                     'textAlign': 'center',
                     'color': colors['text']
                     }),
    html.Div([
            html.Div([
                dcc.Graph(
                id='pie_city',
                figure={
                        'data':data_city,
                        'layout': {
                          'title': "% d'offre par villes",
                          'paper_bgcolor': colors['background'],
                          'font': {
                              'color': colors['text']
                          }
                        },    
                    })
            ], className='four columns'),
            html.Div([
                dcc.Graph(
                id='pie_job',
                figure={
                        'data':data_job,
                        'layout': {
                          'title': "% d'offre par type d'emploi",
                          'paper_bgcolor': colors['background'],
                          'font': {
                              'color': colors['text']
                          }
                        },    
                    }),      
                ], className='four columns'),    
                html.Div([
                dcc.Graph(
                id='pie_salaire',
                figure={
                        'data':data_salaire,
                        'layout': {
                          'title': "% d'offre par type d'emploi",
                          'paper_bgcolor': colors['background'],
                          'font': {
                              'color': colors['text']
                          }
                        },    
                    }),      
                ], className='four columns'),  
    ], className='row')
  ])
