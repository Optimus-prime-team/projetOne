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

colors ={
    'background': '#111111',
    'text': '#7FDBFF'
  }

df =  bdd.load_offers()

df.drop(index = df[df['city_querry'].isnull()].index, inplace = True)

df_paris = df[df['city_querry']== 'Paris']
df_lyon = df[df['city_querry']== 'Lyon']
df_toulouse = df[df['city_querry']== 'Toulouse']
df_nantes = df[df['city_querry']== 'Nantes']
df_bordeau = df[df['city_querry']== 'Paris']

title ="Nombre d'offre scrappées : "+str(len(df))

labels = df.city_querry.unique().tolist()
values = [len(df_paris), len(df_lyon), len(df_toulouse), len(df_nantes), len(df_bordeau)]
#fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

df_buis = df[df['job_querry'] == 'data analyst']

labels_job = df.job_querry.unique().tolist()

nbr_job = []
for elt in labels_job :
    nbr_job.append(len(df[df['job_querry'] == elt]))



data_city = [
    {
        'values': values,
        'type': 'pie',
        'labels' : labels,       
        },
    ]
data_job = [
    {
        'values': nbr_job,
        'type': 'pie',
        'labels' : labels_job,       
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
            ], className='six columns'),
            html.Div([
                dcc.Graph(
                id='pie_job',
                className='six columns',
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
                ], className='six columns'),    
    
    ], className='row')
  ], className='row')