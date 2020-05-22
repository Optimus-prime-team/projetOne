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
cols = ['adId', 'dataJk','city', 'contrat', 'salary','title', 'compagnyName', 
     'description', 'postdate', 'overOneMounth', 'job_querry', 'city_querry']

databaseName   = "mydatabase"
collectionName = "offres_indeed"


def drop_collection() :
    mycol = pymongo.MongoClient()[databaseName][collectionName]
    mycol.drop()

def get_connection() :
    client = pymongo.MongoClient()

    dblist = client.list_database_names()
    if databaseName not in dblist:
        print('db created')
      
    mydb = client[databaseName]
    
    collist = mydb.list_collection_names()
    if collectionName not in collist:
        print('collection created')
    mycol = mydb[collectionName]
    return mycol


def save_offers (liste_offre) :
    
    df_scrappe = pd.DataFrame(liste_offre)
    df_scrappe = df_scrappe.infer_objects() # Convert automatically each dtypes for each columns's dataframe 
    force_del, msg, df_to_add = delete_doublon(df_scrappe)
    if len(df_to_add) != 0 :
        ma_liste = df_to_add.to_dict('records')
        mycol = get_connection()
        x = mycol.insert_many(ma_liste)
        print('ajout de : '+str(len(df_to_add))+ ' elements dans la collection offres_indeed')
    else :
        if force_del == True:
            print(colored('ERROR :'+str(msg), 'red', attrs=["bold"]))
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
        
        df_in_base = pd.DataFrame([['','','','',0.0,'','','','',0,'','']],columns=cols) #TODO rendre la creation du premier dataframe dynamic (dtypes) car si sur la toute premiere page de scrap aucun salaire n'est renseigner l'insertion en base de cette page ne se fera pas.
    try:
        #print(df_scrappe.dtypes)
        #df_scrappe = df_scrappe.infer_objects()
        comparaison_df = df_in_base.merge(df_scrappe,
                                  indicator=True,
                                  how='right')
        diff_df = comparaison_df[comparaison_df['_merge'] != 'both']
        del diff_df['_merge']
        return False, "", diff_df
    except Exception as err:
            return True, err, [] #TODO Corriger ICI car il skip les donnees de la page
    
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






