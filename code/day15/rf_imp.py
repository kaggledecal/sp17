from pandas import DataFrame, Series
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.ensemble import RandomForestClassifier
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

#The Random Forest Model
clf = RandomForestClassifier(n_estimators=100)
clf.fit(local_train_x,local_train_y)
preds = clf.predict_proba(local_test_x)
preds

#Check order of classes
clf.classes_

#Accuracy of Random Forest Model
preds.shape
np.mean((preds[:,1] > 0.5) == local_test_y) #0.83798882681564246

#Feature Importances
local_train.columns.values
clf.feature_importances_

fimps = DataFrame({"fimps": clf.feature_importances_},index=local_train.columns.values[1:])
fimps.plot(kind='bar')

