#!/usr/bin/env python
# coding: utf-8

# ### IMPORT LIBS
import sys
sys.path.append('../preprocess/')
import time
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import preprocess as prepros
from termcolor import colored
from tqdm import tqdm


# ### IMPORT DATABASE

seed = 1
df = prepros._df()

#x = pd.read_csv('../../dbscrap/t3.csv')

#print([col for col in x])
#df = pd.read_csv("../../dbscrap/t2.csv")
#print(df.shape)



#print("X", x)
#print("y", y)
#print(x.shape)
#print(y.shape)
#exit()
#print(data.shape)
#data.to_csv("../../dbscrap/data.csv", index=False)


# ### CHECK CORRELATIONS

#corr = data.corr()
#corr.style.background_gradient(cmap='coolwarm').set_precision(2)

# ### CREATING TRAIN/TEST SET


from sklearn.model_selection import train_test_split

X = df.drop('salary',axis=1)
y = df['salary']

X = X.astype(np.float64, copy=False)
y = y.astype(np.float64, copy=False)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=seed)

print("X_train.shape :",X_train.shape)
print("X_test.shape  :",X_test.shape)
print("y_train.shape :",y_train.shape)
print("y_test.shape  :",y_test.shape)



# ### IMPORT MODELS

from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier, ExtraTreesClassifier, BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import RidgeClassifierCV

from sklearn.feature_selection import SelectFromModel

# ### IMPORT METRICS


from sklearn.metrics import accuracy_score, log_loss, make_scorer, r2_score, mean_squared_error, f1_score, precision_score, jaccard_score, recall_score, roc_auc_score, confusion_matrix, classification_report



"""
#model = GradientBoostingClassifier(random_state=seed)
model = AdaBoostClassifier(random_state=seed)
model.fit(X_train, y_train)

# ### FEATURE SELECTION
thresh = 1e-5#5*10**(-3.5)
selection = SelectFromModel(model, thresh, prefit=True)
X_important_train = selection.transform(X_train)
X_important_test = selection.transform(X_test)

print(X_important_train.shape)
print(X_important_test.shape)
exit()
"""


# ### FEED MODELS AND PARAMETERS
n_jobs = 4

models = [
            'ADB',
            'DTC',
            'GBC',
            'RFC',
            'KNC',
            'SVC',
            'LRG',
            'ETC',
            'BC',
            'RCCV',
         ]
clfs = [
        AdaBoostClassifier(random_state=seed),
        DecisionTreeClassifier(random_state=seed),
        GradientBoostingClassifier(random_state=seed),
        RandomForestClassifier(random_state=seed, n_jobs=n_jobs),
        KNeighborsClassifier(n_jobs=n_jobs),
        SVC(random_state=seed, probability = True),
        LogisticRegression(random_state=seed),
        ExtraTreesClassifier(random_state=seed, n_jobs=n_jobs),
        BaggingClassifier(random_state=seed, n_jobs=n_jobs),
        RidgeClassifierCV(),
        ]

params = {
            models[0]: {'learning_rate':[1, 0.5, 0.1, 0.02, 0.01, 0.002, 0.001],
                        'n_estimators':np.arange(1, 20)},
            models[1]: {'criterion':['gini', 'entropy'],
                        'splitter' : ['best', 'random'],
                        'max_depth':np.arange(1, 20),
                        'min_samples_split':np.arange(2, 20),
                        'min_samples_leaf': np.arange(1, 20)},
            models[2]: {'learning_rate':[1, 0.5, 0.1, 0.02, 0.01, 0.002, 0.001],
                        'n_estimators':np.arange(1, 10),
                        'max_depth':np.arange(1, 5),
                        'min_samples_split':np.arange(2, 5),
                        'min_samples_leaf': np.arange(1, 2)},
            models[3]: {'n_estimators':np.arange(1, 20),
                        'criterion':['gini', 'entropy'],
                        'min_samples_split':np.arange(2, 20),
                        'min_samples_leaf': np.arange(1, 20)},
            models[4]: {'n_neighbors':np.arange(1, 20),
                        'weights':['distance'],
                        'leaf_size':np.arange(1, 30)},
            models[5]: {'C': np.arange(1, 20),
                        'tol':[0.1, 0.01, 0.001],
                        'kernel':['sigmoid', 'linear', 'poly', 'rbf'], 
                        'degree' : np.arange(1, 20)},
            models[6]: {'C':[2000],
                        'tol':[0.1, 0.01, 0.001]},
            models[7]: {'n_estimators':np.arange(1, 20),
                        'max_depth':np.arange(1, 20),
                        'min_samples_split':np.arange(2, 20),
                        'min_samples_leaf': np.arange(1, 2)},
            models[8]: {'n_estimators':np.arange(1, 20)},
            models[9]: {'alpha':[0.001, 0.1, 1.0],
                        'tol':[0.1, 0.01, 0.001],
                        'solver':['auto', 'svd', 'cholesky','lsqr', 'sparse_cg', 'sag', 'saga']},
         }

#scoring = {'AUC': 'roc_auc', 'Accuracy': make_scorer(accuracy_score)}
scoring = {'Accuracy': make_scorer(accuracy_score)}


# ### TRAINING

def training():
    test_scores = []

    for name, estimator in zip(models,clfs):
        print("Training for :",colored(name, "green", attrs=['reverse']))
        startTrain = time.perf_counter()
        
        clf = GridSearchCV(estimator, params[name], scoring=scoring, refit='Accuracy', n_jobs=n_jobs, cv=5, verbose=1, 
                           return_train_score=False)
        clf.fit(X_train, y_train)
        #clf.fit(X_important_train, y_train)
        
        filename = './models/'+name+'_finalized_model_on_db.sav'
        pickle.dump(clf, open(filename, 'wb'))

        print("\n================================================================")
        print("================================================================")
        print(colored("best params: " + str(clf.best_params_), "blue"))
        print(colored("best scores: " + str(clf.best_score_), "cyan"))
        estimates = clf.predict_proba(X_test)
        #estimates = clf.predict_proba(X_important_test)

        y_pred = clf.predict(X_test)
        #y_pred = clf.predict(X_important_test)
        
        acc = accuracy_score(y_test, y_pred)
        #r2 = r2_score(y_test, y_pred)
        #mse = mean_squared_error(y_test, y_pred)
        #rmse = np.sqrt(mse)
        #f1 = f1_score(y_test, y_pred)
        #precisionScore = precision_score(y_test, y_pred)
        #jaccardScore = jaccard_score(y_test, y_pred)
        #recallScore = recall_score(y_test, y_pred)
        #rocAucScore =  roc_auc_score(y_test, y_pred)
        
        
        print("--------------------------------")
        print("Accuracy: {:.4%}".format(acc))
        #print(classification_report(y_test, y_pred))
        #print("F1 : {:.4%}".format(f1))
        #print("MSE : {:.4%}".format(mse))
        #print("RMSE : {:.4%}".format(rmse))
        #print("precision_score : {:.4%}".format(precisionScore))
        #print("jaccard_score : {:.4%}".format(jaccardScore))
        #print("recall_score : {:.4%}".format(recallScore))
        #print("roc_auc_score : {:.4%}".format(rocAucScore))
        #print("R2 : {:.4%}".format(r2))
        print("--------------------------------\n")
        endTrain = time.perf_counter()
        print("time for {} took {}s \n".format(name, colored(endTrain-startTrain, "red")))

        print("================================================================")
        print("================================================================\n")
        
        #test_scores.append((name ,acc, r2, precisionScore, jaccardScore, recallScore, rocAucScore, 
        #                    clf.best_score_, clf.best_params_))




start = time.perf_counter()
training()
end = time.perf_counter()
print("\n\nTotal time {}s ".format(end-start))



#print(test_scores)
