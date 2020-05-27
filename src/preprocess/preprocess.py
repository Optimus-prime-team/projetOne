import re
import sys
import numpy as np
import pandas as pd
sys.path.append('../indeed/')
import mongo_indeed as bdd
from termcolor import colored
from tqdm import tqdm
from joblib import Parallel, delayed

df = bdd.load_offers()

# data Cleaning
df.drop(index = df[df['city_querry'].isnull()].index, inplace = True)

# convert 0.0 to nan
df['salary'] = df['salary'].replace(0, np.nan)

df['contrat'] = df['contrat'].replace(np.nan, "")


print(df.shape)


def _print(el):
    print(colored(el, 'blue'))



def regroupContrat(elementToreplace, replaceBy,df):

    for toReplace in tqdm(elementToreplace, colored("Concat all contrats for {}".format(elementToreplace), "cyan", attrs=["bold"])):
        for _type, _bool in list(zip(df['contrat'], df['contrat'].isnull())):
            if _bool == False:
                if re.search(toReplace, _type):
                    df = df.replace(_type, replaceBy)
    yield df



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




print(df.groupby('contrat').count())
#print(df['contrat'])

#exit()
drop = ['city', 'title', 'description', 'adId', 'dataJk', 'compagnyName', 'description', 'postdate']
df = df.drop(drop, axis=1)

_print("\nDROP COLUMNS "+str(drop)+",\n")


def dummies(data):
    return pd.get_dummies(data)



dfDummies = dummies(df['contrat'])
dfDummiesJob = dummies(df['job_querry'])
dfDummiesCity = dummies(df['city_querry'])
#print(dfDummies.columns)

df = pd.concat([df, dfDummies, dfDummiesJob, dfDummiesCity], axis=1)
df = df.drop(['contrat', 'job_querry', 'city_querry'], axis=1)
print(df)




df.to_csv("/home/fakhredineatallah/Documents/mygit/projects/projetOne/src/preprocess/t.csv", index=False)

def train_test(data, col):
    X = data[data[col].isnull()==False]
    X = X.drop(col, axis=1)
    y = data[data[col].isnull()==True]
    y = y[col]
    return X, y

X, y = train_test(df, 'salary')
print("X", X)
print("y", y)
print(X.shape)
print(y.shape)
