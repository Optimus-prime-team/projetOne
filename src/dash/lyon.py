# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:15:16 2020

@author: utilisateur
"""
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import sys
sys.path.append('../indeed/')
sys.path.append('../preprocess/')
import mongo_indeed as bdd
import preprocess as prepros
import numpy as np
import pandas as pd
import base64
import random
from io import BytesIO

CITY = "Lyon"

colors ={
    'background': '#111111',
    'text': '#7FDBFF'
  }

# df = pd.read_csv('./indeed.csv')
df = prepros.merge_contrat()

# data Cleaning
# df.drop(index = df[df['city_querry'].isnull()].index, inplace = True)

# convert 0.0 to nan
# df['salary'] = df['salary'].replace(0, np.nan)


search_in_city =  df[df['city_querry'] == CITY]


from wordcloud import WordCloud, STOPWORDS

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


stopwords = set(STOPWORDS)
newStopWords = ['job_querry', 'description', 'contrat','city']
stopwords.update(newStopWords)



def plot_wordcloud(data):
    data = data.to_list()
    d = { str(data[i]) : i for i in range(0, len(data) ) }
    wc = WordCloud(
                    background_color='black',
                    stopwords=stopwords,
                    max_words=100,
                    max_font_size=200, 
                    width=1000, height=600,
                    random_state=42,
                    )
    wc.fit_words(d)
    return wc.to_image()

def make_image():
    img = BytesIO()
    plot_wordcloud(data=search_in_city['title']).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())





# mise en place du titre
title ="Nombre d'offre scrappées : "+str(len(search_in_city))


# données pour le pie % d'offre par type d'emploi
search_in_city =  df[df['city_querry'] == CITY]
labels_job = list(search_in_city.groupby('job_querry')['adId'].groups.keys())
nbr_job = search_in_city.groupby('job_querry')['adId'].count().to_numpy().astype(int)

data_job = [
        {
        'values': nbr_job,
        'type': 'pie',
        'labels' : labels_job,       
        },  
     ]



# données pour le pie % d'offre avec salaire
labels_salaire = ['avec salaire', 'sans salaire']
df_avec_salaire = search_in_city[search_in_city['salary'] > 0]
df_sans_salaire = search_in_city[search_in_city['salary'] == 0]

nbr_salaire = [len(df_avec_salaire), (len(search_in_city) - len(df_avec_salaire))]

data_salaire = [
        {
        'values': nbr_salaire,
        'type': 'pie',
        'labels' : labels_salaire,       
        },  
     ]

# données pour le plot bar d'offres les mieux payer dans toute la base et base échantillonner
df_salaire_par_metier = search_in_city[search_in_city['salary'] > 0].groupby('job_querry')
label_j = list(df_salaire_par_metier.groups.keys())


df_mean_salaire_par_metier = df_salaire_par_metier['salary'].mean().to_numpy().astype(int)
df_max_salaire_par_metier = df_salaire_par_metier['salary'].max().to_numpy().astype(int)
df_min_salaire_par_metier = df_salaire_par_metier['salary'].min().to_numpy().astype(int)

data_salaire_par_metier = [
        {
            'x': label_j, 
            'y': df_mean_salaire_par_metier, 
            'type': 'bar', 
            'name': 'moyenne',
            'labels' : 'moyenne',

        },
        {
            'x': label_j,
            'y': df_max_salaire_par_metier, 
            'type': 'bar', 
            'name': 'max',
            'labels' : 'max',
        },
        {
            'x': label_j,
            'y': df_min_salaire_par_metier, 
            'type': 'bar', 
            'name': 'min',
            'labels' : 'min',
        },
    ]



# données pour le plot bar d'offres les mieux payer par type de contrat
df_salaire_par_contrat = search_in_city[search_in_city['salary'] > 0].groupby('contrat')

label_contrat = list(df_salaire_par_contrat.groups.keys())

df_mean_salaire_par_contrat = df_salaire_par_contrat['salary'].mean().astype(int).to_numpy()
df_max_salaire_par_contrat = df_salaire_par_contrat['salary'].max().to_numpy().astype(int)
df_min_salaire_par_contrat = df_salaire_par_contrat['salary'].min().to_numpy().astype(int)

data_salaire_par_contrat = [
        {
            'x': label_contrat, 
            'y': df_mean_salaire_par_contrat, 
            'type': 'bar', 
            'name': 'moyenne'
        },
        {
            'x': label_contrat, 
            'y': df_max_salaire_par_contrat, 
            'type': 'bar', 
            'name': 'max'
        },
        {
            'x': label_contrat, 
            'y': df_min_salaire_par_contrat, 
            'type': 'bar', 
            'name': 'min'
        },
    ]


# données pour le plot bar d'offres qui on plus d'un mois par metier
df_under_one_mounth_par_metier = search_in_city[search_in_city['overOneMounth'] == 0].groupby('job_querry')
label_metier_under_one_mounth = list(df_under_one_mounth_par_metier.groups.keys())
nb_under_one_mounth_par_metier = df_under_one_mounth_par_metier['overOneMounth'].count().to_numpy().astype(int)

df_over_one_mounth_par_metier = search_in_city[search_in_city['overOneMounth'] == 1].groupby('job_querry')
label_metier_over_one_mounth = list(df_over_one_mounth_par_metier.groups.keys())
nb_over_one_mounth_par_metier = df_over_one_mounth_par_metier['overOneMounth'].count().to_numpy().astype(int)

data_over_one_mounth_par_metier = [
        {
            'x': label_metier_over_one_mounth, 
            'y': nb_over_one_mounth_par_metier, 
            'type': 'bar', 
            'name': "plus d'un mois"
        },
        {
            'x': label_metier_under_one_mounth, 
            'y': nb_under_one_mounth_par_metier, 
            'type': 'bar', 
            'name': "moin d'un mois"
        }

    ]


# données pour le plot bar d'offres qui on plus d'un mois par contrat
df_over_one_mounth_par_contrat = search_in_city[search_in_city['overOneMounth'] == 1].groupby('contrat')
label_contrat_over_one_mounth = list(df_over_one_mounth_par_contrat.groups.keys())
nb_over_one_mounth_par_contart = df_over_one_mounth_par_contrat['overOneMounth'].count().to_numpy().astype(int)

df_under_one_mounth_par_contrat = search_in_city[search_in_city['overOneMounth'] == 0].groupby('contrat')
label_contrat_under_one_mounth = list(df_under_one_mounth_par_contrat.groups.keys())
nb_under_one_mounth_par_contart = df_under_one_mounth_par_contrat['overOneMounth'].count().to_numpy().astype(int)


data_over_one_mounth_par_contrat = [
        {
            'x': label_contrat_over_one_mounth, 
            'y': nb_over_one_mounth_par_contart, 
            'type': 'bar', 
            'name': "plus d'un mois"
        },
        {
            'x': label_contrat_under_one_mounth, 
            'y': nb_under_one_mounth_par_contart, 
            'type': 'bar', 
            'name': "moin d'un mois"
        }
    ]




colors ={
    'background': '#111111',
    'text': '#7FDBFF'
  }




def get_content():
  return html.Div([
     html.H1(str(CITY.upper())+" DATA", 
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

    html.Img(src=make_image(), 
                    style={
                            'display': 'block',
                            'margin-left': 'auto',
                            'margin-right': 'auto'
                        }),


    html.H2("Salaires",
                style={
                        'textAlign': 'center',
                        'color': colors['text']
                        }),

    html.Div([
            html.Div([
                dcc.Graph(
                id='bar_salary',
                figure={
                        'data': data_salaire_par_metier,
                        'layout': {
                          'title': "salaire par metier",
                          'paper_bgcolor': colors['background'],
                          'font': {
                              'color': colors['text']
                          }
                        },    
                    })
            ], className='six columns'),
            html.Div([
                dcc.Graph(
                id='bar_salary',
                figure={
                        'data': data_salaire_par_contrat,
                        'layout': {
                          'title': "salaire par contart",
                          'paper_bgcolor': colors['background'],
                          'font': {
                              'color': colors['text']
                          }
                        },    
                    })
            ], className='six columns')                    
    ], className='row'),

    html.H2("Annonces plus d'un mois",
                style={
                        'textAlign': 'center',
                        'color': colors['text']
                        }),


    html.Div([
            html.Div([
                dcc.Graph(
                id='bar_salary',
                figure={
                        'data': data_over_one_mounth_par_metier,
                        'layout': {
                          'title': "Annonces plus d'un mois par metier",
                          'paper_bgcolor': colors['background'],
                          'font': {
                              'color': colors['text']
                          }
                        },    
                    })
            ], className='six columns'),
            html.Div([
                dcc.Graph(
                id='bar_salary',
                figure={
                        'data': data_over_one_mounth_par_contrat,
                        'layout': {
                          'title': "Annonces plus d'un mois par contart",
                          'paper_bgcolor': colors['background'],
                          'font': {
                              'color': colors['text']
                          }
                        },    
                    })
            ], className='six columns')                    
    ], className='row'),

  ])