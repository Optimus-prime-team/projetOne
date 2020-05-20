# -*- coding: utf-8 -*-
"""
Created on Mon May 18 10:49:15 2020

FONCTIONS : 
    
    drop_collection() -> supprimme la collection 'offres_indeed'
    get_connection() -> retourne un curseur sur la collection 'offres_indeed'
    save_offers (liste_offre) -> enregistre la liste d'offre scrappées (voir expl ligne 23) pas de retour
    load_offers () -> retourne un dataFrame de la collection 'offres_indeed'
    delete_doublon(df_scrappe) -> retourne un dataframe des offres scrappées qui ne sont 
                                  pas deja presente dans la collection 'offres_indeed'

@author: MonOrdiPro
"""

import pymongo
import pandas as pd
cols = ['city', 'contrat', 'salary','title', 'compagnyName', 'compagnyLocation', 'description', 'postdate']

"""
# Listes de tests :
mylist = [
  { "entreprise": "Amy2", "poste": "dev data", 'salaire' : 2000, 'lieu' : 'Nantes', 'description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'},
  { "entreprise": "Hannah2", "poste": "data scientist", 'salaire' : '', 'lieu' : 'Paris', 'description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'},
  { "entreprise": "grrr2", "poste": "data scientist", 'salaire' : 5000, 'lieu' : 'Paris','description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'},
]
mylist2 = [
  { "entreprise": "Amy2", "poste": "dev data", 'salaire' : 2000, 'lieu' : 'Nantes', 'description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'},
  { "entreprise": "H", "poste": "data scientist", 'salaire' : '', 'lieu' : 'Paris', 'description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'},
  { "entreprise": "g", "poste": "data scientist", 'salaire' : 5000, 'lieu' : 'Paris','description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'},
]

mylist23 = [
  { "entreprise": "A111", "poste": "dev data", 'salaire' : 2000, 'lieu' : 'Nantes', 'description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'},
  { "entreprise": "H1111", "poste": "data scientist", 'salaire' : '', 'lieu' : 'Paris', 'description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'},
  { "entreprise": "g111", "poste": "data scientist", 'salaire' : 5000, 'lieu' : 'Paris','description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'},
]

df_offre = pd.DataFrame([['A111', "dev data", 2000, 'Nantes', 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'],
                         ['zzzzzz', "dev data", 2000, 'Nantes', 'sghdfhfhfdhdqfhd dfhdqfhdffqdh']], 
    columns=['entreprise', 
                        "poste", 'salaire', 'lieu', 'description'])

liste_offre = [
  { "entreprise": "Amy2", "poste": "dev data", 'salaire' : 2000, 'lieu' : 'Nantes', 'description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'},
  { "entreprise": "H11n1", "poste": "data scientist", 'salaire' : '', 'lieu' : 'Paris', 'description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'},
  { "entreprise": "g1nnn", "poste": "data scientist", 'salaire' : 5000, 'lieu' : 'Paris','description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'},
  { "entreprise": "KKnnnKK", "poste": "data scientist", 'salaire' : 5000, 'lieu' : 'Paris','description' : 'sghdfhfhfdhdqfhd dfhdqfhdffqdh'}
]

"""

def drop_collection() :
    mycol = pymongo.MongoClient("mongodb+srv://nico:root@cluster0-fgi6m.azure.mongodb.net/test?retryWrites=true&w=majority")["mydatabase"]["offres_indeed"]
    mycol.drop()

def get_connection() :
    client = pymongo.MongoClient("mongodb+srv://nico:root@cluster0-fgi6m.azure.mongodb.net/test?retryWrites=true&w=majority")
    #db = client.test
    #myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    dblist = client.list_database_names()
    if "mydatabase" not in dblist:
        print('db created')
      
    mydb = client["mydatabase"]
    
    collist = mydb.list_collection_names()
    if "offres_indeed" not in collist:
        print('collection created')
    mycol = mydb["offres_indeed"]
    return mycol


def save_offers (liste_offre) :
    #df_scrappe = pd.DataFrame(liste_offre)
    df_to_add = delete_doublon(liste_offre)
    if len(df_to_add) != 0 :
        ma_liste = df_to_add.to_dict('records')
        mycol = get_connection()
        x = mycol.insert_many(ma_liste)
        print('ajout de : '+str(len(df_to_add))+ ' elements dans la collection offres_indeed')
    else :
        print('Rien à ajouter !')

def load_offers ():
    mycol = get_connection()
    mylist = mycol.find()
    df = pd.DataFrame(list(mylist))
    
    if len(df) != 0 :
        del df['_id']
    print('il y a actuellement : '+str(len(df))+' elements dans la collection')
    return df

def delete_doublon(df_scrappe):
    
    df_in_base = load_offers()
    if len(df_in_base) == 0 :
        df_in_base = pd.DataFrame([['','','','','','','','']],columns=cols, dtype='str')
    comparaison_df = df_in_base.merge(df_scrappe,
                              indicator=True,
                              how='right')
    diff_df = comparaison_df[comparaison_df['_merge'] != 'both']
    del diff_df['_merge']
    return diff_df



#drop_collection()

#x = load_offers()

"""
save_offers (mylist)
save_offers (mylist2)  
save_offers (mylist23)
save_offers (liste_offre)


x = load_offers()
"""
