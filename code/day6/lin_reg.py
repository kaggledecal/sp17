from pandas import DataFrame, Series
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.cross_validation import train_test_split

#Read in Wine Data
wine = pd.read_csv("../../datasets/wine/wine.csv")

#Data Exploration
wine.shape
wine.head()
wine.info()

wine.corr()

#Train Test Splitting
local_train, local_test = train_test_split(wine,test_size=0.2,random_state=123)
local_train.shape
local_test.shape

local_train_y = local_train["Price"]
local_train_x = local_train.drop(["Price"],axis=1)
local_test_y = local_test["Price"]
local_test_x = local_test.drop("Price",axis=1)

#The Model
clf = sm.OLS(local_train_y,local_train_x)
result = clf.fit()
preds = result.predict(local_test_x)

#MSE of Linear Model
np.sum((local_test_y.values - preds)**2)



#Coefficients are not as readily interpretable
result.summary()

#Highly correlated variables confuse linear models
wine.corr() #Year, Age, and Population of France are heavily correlated. Let's leave out Year and Population of France

wine2 = wine.drop(["Year","FrancePop"],axis=1)

local_train, local_test = train_test_split(wine2,test_size=0.2,random_state=123)
local_train.shape
local_test.shape

local_train_y = local_train["Price"]
local_train_x = local_train.drop(["Price"],axis=1)
local_test_y = local_test["Price"]
local_test_x = local_test.drop("Price",axis=1)

clf = sm.OLS(local_train_y,local_train_x)
result = clf.fit()
preds = result.predict(local_test_x)

#MSE of Linear Model
np.sum((local_test_y.values - preds)**2)

result.summary() #Notice there is no more warning on multicollinearity!










