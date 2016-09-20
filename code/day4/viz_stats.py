from pandas import DataFrame, Series
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import missingno as msno

#~/anaconda/bin/pip install missingno



#Read in Data
df = pd.read_csv('~/src/kaggledecal/datasets/titanic/train.csv')

#Data diagnostics
df.shape
df.head()
df.describe()
df.dtypes
df.describe(include=['O'])

df.columns
df.index

df['Survived'].mean()
df.groupby('Sex')['Survived'].mean() #Groupby groups dataframe with selected variables so you can perform statistics on each group
df.groupby('Sex')['Survived'].size() #Size counts the number in each group

df.corr()
df.groupby('Pclass')['Survived'].mean()

df['Fare_bins'] = pd.cut(df['Fare'],bins=[0,20,50,80,1000]) #Categorizing numerical data into bins for easy groupby
df.groupby('Fare_bins')['Survived'].mean()
df.groupby(['Sex','Fare_bins'])['Survived'].mean()
df.groupby(['Sex','Fare_bins'])['Survived'].agg([np.mean,np.size,np.std])


df.isnull().sum() #Counts missing values for each column

def countInfs(series):
	#Counts infinite values for a particular column
	if (series.dtype == 'int64') | (series.dtype == 'float64'):
		return sum((series > 1e20) | (series < -1e20))
	else:
		return 0

df.select_dtypes(include=[np.number]).apply(countInfs,axis=0)

df['SibSp'].value_counts() #Tabulates counts of each unique value

#Data Visuals
df['Age'].hist(bins=20)
plt.title('Distribution of All Ages')
plt.xlabel('Age')
plt.ylabel('Counts')

df.groupby('Sex')['Age'].hist(bins=20,alpha=0.5)
plt.legend(labels=['Female','Male'])
plt.title('Distribution of Ages by Female and Male')

df.groupby('Sex')['Age'].plot(kind='density')
plt.legend(labels=['Female','Male'])
plt.title('Distribution of Ages by Female and Male')

colors = ['blue','green','yellow']
plt.scatter(df['Age'],df['Fare'],c=df[df.Age.notnull()]['Pclass'].apply(lambda x: colors[x-1]),alpha=0.5)
plt.xlabel('Age')
plt.ylabel('Fare Price')
plt.title('Scatterplot of Fare Price vs. Age Colored by Class')

#Subplots
fig, axes = plt.subplots(2,1)
df.Embarked.value_counts().plot(ax=axes[0],kind='bar')
df.groupby('Embarked')['Age'].mean().plot(ax=axes[1],kind='bar')
axes[0].set_title("Number of Passengers per Location")
axes[1].set_title("Mean Age per Location")
axes[1].set_xlabel("Location")
axes[0].set_ylabel("Counts")
axes[1].set_ylabel("Proportion")

#Prettier Plots
import seaborn as sns

sns.set_style("white")

fig, axes = plt.subplots(2,1)
df.Embarked.value_counts().plot(ax=axes[0],kind='bar')
df.groupby('Embarked')['Age'].mean().plot(ax=axes[1],kind='bar')
axes[0].set_title("Number of Passengers per Location")
axes[1].set_title("Mean Age per Location")
axes[1].set_xlabel("Location")
axes[0].set_ylabel("Counts")
axes[1].set_ylabel("Proportion")

sns.stripplot(x="Embarked", y="Age", hue='Sex', data=df, jitter=True);
sns.plt.title("Strip Plot with Seaborn")

#Visualizing Missing Values
msno.matrix(train)





































