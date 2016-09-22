
from pandas import DataFrame, Series
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#Filling in Missing Values
df = pd.read_csv('~/src/kaggledecal/datasets/titanic/train.csv')
df['Age'].fillna(df.Age.mean(),inplace=True)

df = pd.read_csv('~/src/kaggledecal/datasets/titanic/train.csv')
df['title'] = 'other'
df.loc[['Master.' in n for n in df['Name']],'title'] = 'Master'
df.loc[['Miss.' in n for n in df['Name']],'title'] = 'Miss'
df.loc[['Mr.' in n for n in df['Name']],'title'] = 'Mr'
df.loc[['Mrs.' in n for n in df['Name']],'title'] = 'Mrs'

#-Brief aside --
	#loc vs. iloc vs. ix
	#use loc if you plan on indexing by the index label of a dataframe, e.g.
	df.head()
	#the left most column represents the index and so if you do df.loc[1] you will select the second row
	#but say the index was like so:
	df_copy = df.copy()
	df_copy.index = pd.Index(df.index.values-1)
	df_copy.head()
	df_copy.loc[1]
	#since the index of 1 correponds to the third row, loc will select the third row 

	#iloc will index on position (actual row number) starting with 0 for the first row regardless of index
	df.iloc[1]
	df_copy.iloc[1]

	#ix defaults to behave like loc but falls back to iloc if a label is not in the index AND if the index contains both strings and numerics
	#in most cases, you will use loc and iloc more often than ix. ix is useful if you want to index the rows by index label and columns
	#by position 
	df.ix[:3,:2]
	df_copy.ix[:3,:2]
#-

df.boxplot(column='Age',by='title') #Mean Age is different per title
plt.ylabel('Age')

df['age_filled'] = df[['title','Age']].groupby('title').transform(lambda x: x.fillna(x.mean())) #Transform performs operation per group and returns values to their original index
df[['title','Age','age_filled']].tail(20)
df.groupby('title')['Age'].mean()

df['Cabin'] 
#Cabin number can distinguish between port or starboard side of the Titanic. From research, it seems that
#the "Women and children first" policy was implemented differently between the two sides. The starboard side
#had women and children prioritized before letting men on board while the port side ONLY allowed women and
#children on board. Odd cabin numbers were on the starboard side and even cabin numbers were on the port side.

#Cabin letter designates the deck on the titanic, starting from highest to lowest - A to G. 

df['cabin_side'] = 'Unknown'
df.loc[df['Cabin'].str[-1].isin(["1", "3", "5", "7", "9"]),'cabin_side'] = 'starboard'
df.loc[df['Cabin'].str[-1].isin(["2", "4", "6", "8", "0"]),'cabin_side'] = 'port'
df['cabin_side'].value_counts()

df['deck'] = 'Unknown'
df.loc[df['Cabin'].notnull(),'deck'] = df['Cabin'].str[0]
df['deck'].value_counts()
df[df['Cabin'].str[0]=='T'] #Why is there a T deck...
df.loc[df['deck'] == 'T','deck'] = "Unknown"

#Some cabins start with "F" followed by a space and then the actual deck letter
df['Cabin'][df.Cabin.notnull()].values

#Regular Expression Assignment!!!!!!!!!!!!!!!!


pattern = "[A-Z]\s[A-Z]" #Any capital letter between A-Z followed by a whitespace followed by any letter between A-Z
mask = df['Cabin'].str.contains(pattern,na=False)
df.loc[mask,'Cabin']
df.loc[mask,'deck'] = df.loc[mask,'Cabin'].str[2]
df.deck.value_counts()

#If you also look closely, some people have multiple cabins assigned to them possibly indicating group tickets for the family
#We can split these by whitespace and count them to make another variable called "number_in_group"
df['Cabin'].str.split()
df['num_in_group'] = df['Cabin'].str.split().apply(lambda x: len(x) if type(x)!=float else 1)
df.loc[25:30]

# Home Depot Data Set
import re #For regular expressions

hd = pd.read_csv("~/src/kaggle_decal/datasets/home_depot/train.csv", encoding="ISO-8859-1")

strNum = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9} #Used to convert spelled out numbers to the actual digits


#And here's the list of regex! Credits to the1owl on Kaggle for compiling all of this

hd['cleaned_product_title'] = hd['product_title'].map(lambda s: re.sub(r"(\w)\.([A-Z])", r"\1 \2", s)) #Split words with a.A
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.lower())
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("  "," "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace(",","")) #could be number / segment later
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("$"," "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("?"," "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("-"," "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("//","/"))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("..","."))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace(" \\ "," "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("."," . "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"(^\.|/)", r"", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"(\.|/)$", r"", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9])([a-z])", r"\1 \2", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([a-z])([0-9])", r"\1 \2", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace(" x "," xbi "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([a-z])( *)\.( *)([a-z])", r"\1 \4", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([a-z])( *)/( *)([a-z])", r"\1 \4", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("*"," xbi "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace(" by "," xbi "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9])( *)\.( *)([0-9])", r"\1.\4", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(inches|inch|in|')\.?", r"\1in. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(foot|feet|ft|'')\.?", r"\1ft. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(pounds|pound|lbs|lb)\.?", r"\1lb. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(square|sq) ?\.?(feet|foot|ft)\.?", r"\1sq.ft. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(cubic|cu) ?\.?(feet|foot|ft)\.?", r"\1cu.ft. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(gallons|gallon|gal)\.?", r"\1gal. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(ounces|ounce|oz)\.?", r"\1oz. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(centimeters|cm)\.?", r"\1cm. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(milimeters|mm)\.?", r"\1mm. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("°"," degrees "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(degrees|degree)\.?", r"\1deg. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace(" v "," volts "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(volts|volt)\.?", r"\1volt. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(watts|watt)\.?", r"\1watt. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: re.sub(r"([0-9]+)( *)(amperes|ampere|amps|amp)\.?", r"\1amp. ", s))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("  "," "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace(" . "," "))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: (" ").join([str(strNum[z]) if z in strNum else z for z in s.split(" ")]))
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.lower())
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("toliet","toilet")) 
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("airconditioner","air conditioner")) 
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("vinal","vinyl")) 
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("vynal","vinyl")) 
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("skill","skil")) 
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("snowbl","snow bl")) 
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("plexigla","plexi gla")) 
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("rustoleum","rust-oleum")) 
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("whirpool","whirlpool")) 
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("whirlpoolga", "whirlpool ga")) 
hd['cleaned_product_title'] = hd['cleaned_product_title'].map(lambda s: s.replace("whirlpoolstainless","whirlpool stainless")) 


#In order to better understand what each line does, let's break this down a bit:
s = re.sub(r"(\w)\.([A-Z])", r"\1 \2", s) #Split words with a.A

#The prefix "r" represents that whatever comes next should be interpretted as a "raw string" 
#Since python tries to be smart and convert, say, "\b" to mean "backspace" for you, this won't be converted correctly in regex.
#Prefixing your regex patterns with "r" will tell python to hand over the "raw string" pattern for normal regex to work.

#The "\1" code means "take the first regex group in parantheses and put it here". In this example, we put whatever word character
#"(\w)" captures into the \1 spot and whatever capital letter "([A-Z])" catures into the \2 spot.

pattern = r"(\w)\.([A-Z])"
matches = hd.product_title.str.contains(pattern)
hd.product_title.iloc[np.where(matches)]

s = hd.product_title.iloc[73970]
s
s = re.sub(r"(\w)\.([A-Z])", r"\1 \2", s)
s

#FB Data for Date Columns
fb = pd.read_csv("~/src/kaggle_decal/datasets/fb/train.csv")

fb.head()

initial_date = np.datetime64('2014-01-01T01:01', dtype='datetime64[m]')  #Arbitrary start date
d_times = pd.DatetimeIndex(initial_date + np.timedelta64(int(mn), 'm') for mn in fb.time.values)    
d_times[:5]

fb['hour'] = d_times.hour
fb['weekday'] = d_times.weekday 
fb['day'] = d_times.day 
fb['month'] = d_times.month
fb['year'] = d_times.year









