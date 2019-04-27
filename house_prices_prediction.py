# -*- coding: utf-8 -*-
"""House_Prices_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Gr5krLSuw1hZE5OzU-vdqrg8AyYtWOaM
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from google.colab import files
uploaded = files.upload()

import io
train_data = pd.read_csv(io.BytesIO(uploaded['train.csv']))

train_data.shape

train_data.head(20)

corr=train_data.corr()

corr.style.background_gradient(cmap='coolwarm')

#there are categorical values too we have to encode them
#splitting the data into train and test
x=train_data.iloc[:,1:-1]
y=train_data.iloc[:,-1]

x.isnull().sum()

#now we have to deal with missing values
col=[c for c in train_data.columns if train_data[c].isnull().any()]
for i in col:
    if(x[i].dtype == np.dtype('O')):
        x[i]=x[i].fillna(x[i].value_counts().index[0])
    else:
        x[i]=x[i].fillna(x[i].mean())

x.isnull().sum()

from sklearn.preprocessing import LabelEncoder
lb=LabelEncoder()
for c in x.select_dtypes(include="object"):
    x[c]=lb.fit_transform(x[c])

x_train

x.head()

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.1,random_state=0)
#applying the model
from sklearn.ensemble import RandomForestRegressor
r=RandomForestRegressor(n_estimators=30,min_samples_split=5)
r.fit(x_train,y_train)
y_pred=r.predict(x_test)
from sklearn.metrics import r2_score
r2_score(y_test,y_pred)

#applying another algorithm
from sklearn import tree
t=tree.DecisionTreeRegressor(min_samples_leaf=10,min_samples_split=6)
t.fit(x_train,y_train)
y_pred1=t.predict(x_test)
from sklearn.metrics import r2_score
r2_score(y_test,y_pred1)

test_data=pd.read_csv('test.csv')

test_data.head()

test_data.isnull().sum()

#we have to deal with null values
test_data=test_data.iloc[:,1:]
k=[c for c in test_data.columns if test_data[c].isnull().any()]
for i in k:
    if(test_data[i].dtype == np.dtype('O')):
        test_data[i]=test_data[i].fillna(test_data[i].value_counts().index[0])
    else:
        test_data[i]=test_data[i].fillna(test_data[i].mean())

for c in test_data.select_dtypes(include="object"):
    test_data[c]=lb.fit_transform(test_data[c])

test_data.head()

list(set(test_data.columns)-set(x_test.columns))

len(test_data.columns)

len(x_test.columns)

prediction=r.predict(test_data)

ss = pd.read_csv('sample_submission.csv')

output = pd.DataFrame({'Id': ss.Id,'SalePrice': prediction})
output.to_csv('submission.csv', index=False)
output.head()



