# -*- coding: utf-8 -*-
"""
Created on Mon May 18 10:49:15 2020

FONCTIONS : 
    
    drop_collection() -> supprimme la collection 'offres_indeed'
    get_connection() -> retourne un curseur sur la collection 'offres_indeed'
    save_offers (liste_offre) -> enregistre la liste d'offre scrappées (voir expl ligne 23) pas de retour
    load_offers () -> retourne un dataFrame de la collection 'offres_indeed'

@author: MonOrdiPro
"""

import pymongo
import pandas as pd
from termcolor import colored

DATABASENAME   = "indeed_b"
collection_indeed_offers  = "offres_indeed"
collection_indeed_history = "offres_indeed_slave"

def get_connection(databaseName, collectionName) :
    #client = pymongo.MongoClient("mongodb+srv://Fakhredine:4jM92%2Aqh%23fw3@cluster0-4chav.mongodb.net/test?retryWrites=true&w=majority")
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
    collection = get_connection(DATABASENAME, collection_indeed_offers)
    collection1 = get_connection(DATABASENAME, collection_indeed_history)
    a = df_scrappe.to_dict('records')[0]
    findIfexist = collection.find_one({'adId' : a['adId']}, { })
   
    try:
        if findIfexist != None:
            mongoId = findIfexist['_id']
            collection.find_one_and_update(
                    {"_id": mongoId},
                    {
                    "$set": {
                             "adId"         : a['adId'],
                             "dataJk"       : a['dataJk'],
                             "compagnyName" : a['compagnyName'],
                             "job_querry"   : a['job_querry'],
                             "salary"       : a['salary'],
                             "title"        : a['title'],
                             "contrat"      : a['contrat'],
                             "description"  : a['description'],
                             "title"        : a['title'],
                             "scrapDate"    : a['scrapDate'],
                             "postdate"     : a['postdate'],
                             "city_querry"  : a['city_querry'],
                             "overOneMounth": a['overOneMounth']
                             }
                    },
                )
            collection1.insert_one(a)
            return colored("update DONE", "yellow", attrs=["bold"])

        else:
            collection.insert_one(a)
            collection1.insert_one(a)
            return colored("insert Done", "blue", attrs=["bold"])

    except:
        return colored("NO","red", attrs=["bold"])

    
def load_offers ():
    mycol = get_connection(DATABASENAME, collection_indeed_offers)
    mylist = mycol.find()
    df = pd.DataFrame(list(mylist))
    
    if len(df) != 0 :
        del df['_id']
    print('il y a actuellement : '+str(len(df))+' elements dans la collection')
    return df


def history():
    mycol = get_connection(DATABASENAME, collection_indeed_history)
    mylist = mycol.find()

    #TODO regarder l'history
    print("")
