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
from termcolor import colored
#cols = ['entreprise', "poste", 'salaire', 'lieu', 'description']
cols = ['city', 'contrat', 'salary','title', 'compagnyName', 
        'description', 'postdate', 'overOneMounth', 'job_querry', 'city_querry']



def drop_collection() :
    mycol = pymongo.MongoClient()["mydatabase"]["offres_indeed"]
    mycol.drop()

def get_connection() :
    client = pymongo.MongoClient()
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
    df_scrappe = pd.DataFrame(liste_offre)
    force_d, df_to_add = delete_doublon(df_scrappe)
    if len(df_to_add) != 0 :
        ma_liste = df_to_add.to_dict('records')
        mycol = get_connection()
        x = mycol.insert_many(ma_liste)
        print('ajout de : '+str(len(df_to_add))+ ' elements dans la collection offres_indeed')
    else :
        if force_d == True:
            print(colored('WARNING force to not insert in DB -Rien à ajouter !', 'yellow'))
        else:
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
        df_in_base = pd.DataFrame([['','','','','','','','','','']],columns=cols)
    try:
        comparaison_df = df_in_base.merge(df_scrappe,
                                  indicator=True,
                                  how='right')
        diff_df = comparaison_df[comparaison_df['_merge'] != 'both']
        del diff_df['_merge']
        return False, diff_df
    except:
        # TODO "ValueError: You are trying to merge on float64 and object columns. If you wish to proceed you should use pd.concat" URGENT corriger ici
        return True, [] #TODO Corriger ICI car il skip les donnees de la page
    
    #return diff_df, force_d



#drop_collection()

x = load_offers()

"""
save_offers (mylist)
save_offers (mylist2)  
save_offers (mylist23)
save_offers (liste_offre)


x = load_offers()
"""

sal = 200






