# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:15:16 2020

@author: utilisateur
"""
import pandas as pd
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


search_in_nantes =  df[df['city_querry'] == "Nantes"]

# mise en place du titre
title ="Nombre d'offre scrappées : "+str(len(search_in_nantes))


# données pour le pie % d'offre par type d'emploi
search_in_nantes =  df[df['city_querry'] == "Nantes"]
labels_job = list(search_in_nantes.groupby('job_querry')['adId'].groups.keys())
nbr_job = search_in_nantes.groupby('job_querry')['adId'].count().to_numpy().astype(int)

data_job = [
        {
        'values': nbr_job,
        'type': 'pie',
        'labels' : labels_job,       
        },  
     ]



# données pour le pie % d'offre avec salaire
labels_salaire = ['avec salaire', 'sans salaire']
df_avec_salaire = search_in_nantes[search_in_nantes['salary'] > 0]
df_sans_salaire = search_in_nantes[search_in_nantes['salary'] == 0]

# print(avec_salaire)
# exit()
# df_avec_salaire = df[df['salary'].isnull()==False]

nbr_salaire = [len(df_avec_salaire), (len(search_in_nantes) - len(df_avec_salaire))]

data_salaire = [
        {
        'values': nbr_salaire,
        'type': 'pie',
        'labels' : labels_salaire,       
        },  
     ]

# données pour le plot bar d'offres les mieux payer dans toute la base et base échantillonner
df_mean_salaire_par_cat = search_in_nantes[search_in_nantes['salary'] > 0].groupby('job_querry')
label_j = list(df_mean_salaire_par_cat.groups.keys())

# print(label_j)
df_mean_salaire_par_cat = df_mean_salaire_par_cat['salary'].mean().to_numpy().astype(int)

# print(df_mean_salaire_par_cat)


# exit()
data_salaire_par_metier = [
        {
            'x': label_j, 
            'y': df_mean_salaire_par_cat, 
            'type': 'bar', 
            'name': label_j
        },
        {
            'x': [1, 2, 3], #TODO finir ici sur le dataset reequilibré
            'y': [2, 4, 5], 
            'type': 'bar', 
            'name': u'Montréal'
        },
    ]



colors ={
    'background': '#111111',
    'text': '#7FDBFF'
  }




def get_content():
  return html.Div([
     html.H1("NANTES DATA", 
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
                ], className='six columns'),    
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
                ], className='six columns'),  
    ], className='row'),




    html.Div([
            html.Div([
                dcc.Graph(
                id='bar_salary',
                figure={
                        'data': data_salaire_par_metier,
                        'layout': {
                          'title': "salaire les mieux payer par metier",
                          'paper_bgcolor': colors['background'],
                          'font': {
                              'color': colors['text']
                          }
                        },    
                    })
            ], className='six columns')                
    ], className='row'),
  ])