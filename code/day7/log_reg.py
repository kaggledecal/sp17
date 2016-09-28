from pandas import DataFrame, Series
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.cross_validation import train_test_split


#Read in Titanic Data
titanic = pd.read_csv("../../datasets/titanic/train.csv")

titanic_only = pd.get_dummies(titanic,columns=['Sex','Pclass','Embarked'],drop_first=True)

#Drop columns we don't care about (yet) or have missing values (Models don't like missing values)
titanic_only.drop(['PassengerId','Name','Ticket','Age','Cabin'],axis=1,inplace=True)

#Train Test Splitting
local_train, local_test = train_test_split(titanic_only,test_size=0.2,random_state=123)
local_train.shape
local_test.shape

local_train_y = local_train["Survived"]
local_train_x = local_train.drop(["Survived"],axis=1)
local_test_y = local_test["Survived"]
local_test_x = local_test.drop("Survived",axis=1)

#The Model
clf = sm.Logit(local_train_y,local_train_x)
result = clf.fit()
preds = result.predict(local_test_x)

#Accuracy of Logistic Model
np.mean((preds > 0.5) == local_test_y)

result.summary()




#Read in Titanic Data (Feature Engineered)
titanic = pd.read_csv("../../datasets/titanic/train.csv")

titanic_engineered = titanic.copy()
#Imputing Age
titanic_engineered['title'] = 'other'
titanic_engineered.loc[['Master.' in n for n in titanic_engineered['Name']],'title'] = 'Master'
titanic_engineered.loc[['Miss.' in n for n in titanic_engineered['Name']],'title'] = 'Miss'
titanic_engineered.loc[['Mr.' in n for n in titanic_engineered['Name']],'title'] = 'Mr'
titanic_engineered.loc[['Mrs.' in n for n in titanic_engineered['Name']],'title'] = 'Mrs'

titanic_engineered['age_filled'] = titanic_engineered[['title','Age']].groupby('title').transform(lambda x: x.fillna(x.mean())) #Transform performs operation per group and returns values to their original index
titanic_engineered.drop(['Age'],axis=1,inplace=True)

#Cabin Side Feature
titanic_engineered['cabin_side'] = 'Unknown'
titanic_engineered.loc[titanic_engineered['Cabin'].str[-1].isin(["1", "3", "5", "7", "9"]),'cabin_side'] = 'starboard'
titanic_engineered.loc[titanic_engineered['Cabin'].str[-1].isin(["2", "4", "6", "8", "0"]),'cabin_side'] = 'port'

#Deck Feature (including some cleaning)
titanic_engineered['deck'] = 'Unknown'
titanic_engineered.loc[titanic_engineered['Cabin'].notnull(),'deck'] = titanic_engineered['Cabin'].str[0]
titanic_engineered.loc[titanic_engineered['deck'] == 'T','deck'] = "Unknown"

pattern = "[A-Z]\s[A-Z]" #Any capital letter between A-Z followed by a whitespace followed by any letter between A-Z
mask = titanic_engineered['Cabin'].str.contains(pattern,na=False)
titanic_engineered.loc[mask,'deck'] = titanic_engineered.loc[mask,'Cabin'].str[2]

#Number cabins per person
titanic_engineered['num_in_group'] = titanic_engineered['Cabin'].str.split().apply(lambda x: len(x) if type(x)!=float else 1)

#Removing columns we don't want (that don't make sense to include anymore)
titanic_engineered.drop(['PassengerId','Name','Ticket','Cabin','title'],axis=1,inplace=True)

titanic_engineered = pd.get_dummies(titanic_engineered,columns=['Sex','Pclass','Embarked','cabin_side','deck'],drop_first=True)


#Train Test Splitting
local_train, local_test = train_test_split(titanic_engineered,test_size=0.2,random_state=123)
local_train.shape
local_test.shape

local_train_y = local_train["Survived"]
local_train_x = local_train.drop(["Survived"],axis=1)
local_test_y = local_test["Survived"]
local_test_x = local_test.drop("Survived",axis=1)

#The Model
clf = sm.Logit(local_train_y,local_train_x)
result = clf.fit()
preds = result.predict(local_test_x)

#Accuracy of Logistic Model
np.mean((preds > 0.5) == local_test_y)

result.summary()



#Cross Validated instead of Validation Method
from sklearn.cross_validation import KFold

#Splits data into our train and test indices for each fold
kf = KFold(titanic_only.shape[0], n_folds=10)

#Saves our accuracy scores for each fold
outcomes = []

#Keeps track of which fold we are currently in
fold = 0

%cpaste
for train_index, test_index in kf:
    fold += 1
    local_train_xy, local_test_xy = titanic_only.iloc[train_index], titanic_only.iloc[test_index]
    local_train_y = local_train_xy['Survived']
    local_train_x = local_train_xy.drop(['Survived'],axis=1)
    local_test_y = local_test_xy['Survived']
    local_test_x = local_test_xy.drop(['Survived'],axis=1)

    clf = sm.Logit(local_train_y,local_train_x)
    result = clf.fit()
    preds = result.predict(local_test_x)
    accuracy = np.mean((preds > 0.5) == local_test_y)

    outcomes.append(accuracy)
    print("Fold {0} accuracy: {1}".format(fold, accuracy)) 
--

mean_outcome = np.mean(outcomes)
mean_outcome


#Cross Validated with Feature Engineered Data

#Saves our accuracy scores for each fold
outcomes = []

#Keeps track of which fold we are currently in
fold = 0

%cpaste
for train_index, test_index in kf:
    fold += 1
    local_train_xy, local_test_xy = titanic_engineered.iloc[train_index], titanic_engineered.iloc[test_index]
    local_train_y = local_train_xy['Survived']
    local_train_x = local_train_xy.drop(['Survived'],axis=1)
    local_test_y = local_test_xy['Survived']
    local_test_x = local_test_xy.drop(['Survived'],axis=1)

    clf = sm.Logit(local_train_y,local_train_x)
    result = clf.fit()
    preds = result.predict(local_test_x)
    accuracy = np.mean((preds > 0.5) == local_test_y)

    outcomes.append(accuracy)
    print("Fold {0} accuracy: {1}".format(fold, accuracy)) 
--

mean_outcome = np.mean(outcomes)
mean_outcome






