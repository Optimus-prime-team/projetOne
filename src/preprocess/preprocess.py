import os.path
import re
import sys
import numpy as np
import pandas as pd
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
sys.path.append('../indeed/')
import mongo_indeed as bdd
from termcolor import colored
from tqdm import tqdm
from joblib import Parallel, delayed
from os import path


def load():
    print(path.exists('./indeed.csv'))
    # exit()
    if path.exists('./indeed.csv') == True:
        df = pd.read_csv('./indeed.csv')
        print("if")
        
    else:
        print("else")
        df = bdd.load_offers()
    # data Cleaning
    df.drop(index = df[df['city_querry'].isnull()].index, inplace = True)

    # convert 0.0 to nan
    #df['salary'] = df['salary'].replace(0, np.nan)

    df['contrat'] = df['contrat'].replace(np.nan, "no_contrat")
    df['contrat'] = df['contrat'].replace("", "no_contrat")
    # df['salary'] = df['salary'].replace(df[df['salary'] < 500], 0)
    a = np.array(df['salary'].values.tolist())
    df['salary'] = np.where(a > 0 , 0, a).tolist()
    df['salary'] = np.where(a < 1000 , 0, a).tolist()
    # print(df['salary'].shape)
    # print(df['salary'].replace(df[df['salary'] > 500], 0).shape)
    # print(df)


    return df

# print(df.shape)


def _print(el):
    print(colored(el, 'blue'))



def regroupContrat(elementToreplace, replaceBy,df):

    for toReplace in tqdm(elementToreplace, colored("Regroup all contrats for {} in {}".format(elementToreplace, replaceBy), "cyan", attrs=["bold"])):
        for _type, _bool in list(zip(df['contrat'], df['contrat'].isnull())):
            if _bool == False:
                if re.search(toReplace, _type):
                    df = df.replace(_type, replaceBy)
    yield df


def merge_contrat():
    df = load()
    elementToreplace = ["Apprentissage", "Contrat", "Stage"]
    replaceBy = "Apprentissage"
    df = next(regroupContrat(elementToreplace, replaceBy, df))


    elementToreplace = ["CDI", "Temps plein", "Temps partiel"]
    replaceBy = "CDI"
    df = next(regroupContrat(elementToreplace, replaceBy, df))


    elementToreplace = ["Freelance"]
    replaceBy = "Freelance"
    df = next(regroupContrat(elementToreplace, replaceBy, df))


    elementToreplace = ["CDD"]
    replaceBy = "CDD"
    df = next(regroupContrat(elementToreplace, replaceBy, df))


    elementToreplace = ["no_contrat"]
    replaceBy = "no_contrat"
    df = next(regroupContrat(elementToreplace, replaceBy, df))
    df.to_csv('indeed.csv')
    return df

# df = merge_contrat()

# print(df.groupby('contrat').count())
def drop(df):
    drop = ['adId', 'dataJk', 'city', 'title', 'description', 'description', 'overOneMounth', 'postdate', 'scrapDate']
    df = df.drop(drop, axis=1)
    return drop

# _print("\nDROP COLUMNS "+str(drop)+",\n")


def dummies(data):
    return pd.get_dummies(data)

def encode(data):
    values = np.asarray(data)
    #print(values)
    #exit()
    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    #print(integer_encoded)
    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    #print(onehot_encoded)
    return integer_encoded, onehot_encoded



#TODO fisish this function
def decode(data):
    inverted = label_encoder.inverse_transform([argmax(onehot_encoded[0, :])])
    print(inverted)


def hot_encode(df):
    dfDummiesContrat = dummies(df['contrat'])
    dfDummiesJob = dummies(df['job_querry'])
    dfDummiesCity = dummies(df['city_querry'])
    dfIntergerEncodeCompagny, dfOnehotEncodeCompagny = encode(df['compagnyName'])
    dfOnehotEncodeCompagny = pd.DataFrame(dfIntergerEncodeCompagny, columns=['compagnyNameEncoded'])
    """
    print("dfDummiesJob type :", type(dfDummiesJob))
    print("dfDummiesJob :",dfDummiesJob)
    print("dfIntergerEncodeCompagny :",dfIntergerEncodeCompagny)
    print("dfIntergerEncodeCompagny type :",type(dfIntergerEncodeCompagny))
    print("dfOnehotEncodeCompagny :",dfOnehotEncodeCompagny)
    print("dfIntergerEncodeCompagny type :",type(dfOnehotEncodeCompagny))
    exit()
    """

    #print(dfDummies.columns)

    df = pd.concat([df, dfDummiesContrat, dfDummiesJob, dfDummiesCity, dfOnehotEncodeCompagny], axis=1)
    df = df.drop(['contrat', 'compagnyName', 'job_querry', 'city_querry'], axis=1)
    return df

# print(df.columns)
# print(df.shape)
# print(df)

#print(df[df['contrat'] == "Freelance"])
#exit()




# df.to_csv("/home/fakhredineatallah/Documents/mygit/projects/projetOne/dbscrap/t3.csv", index=False)


#TODO ajouter un menu pour demande on veux obtenir les deniers scrap a jour sinon prendre le csv cree
def _df():
    return merge_contrat()


def data(col, seed):
    x = df[df[col].isnull()==False]
    y = df[df[col].isnull()==True]
    percent =  x.shape[0]/y.shape[0]
    y = y.sample(n=(round(percent*y.shape[0])), random_state=seed)
    
    x = x.drop(col, axis=1)
    y = y.drop(col, axis=1)
    #data = pd.concat([x, y], axis=0)
    return  x, y