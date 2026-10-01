# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:29:09 2026

@author: mahat
"""

##Naive bayes Algorithrm
import pandas as pd
data=pd.read_csv(r"C:\Users\mahat\Downloads\spam.csv",encoding='latin-1')
print(data.head())
      
x=data.iloc[ : ,1].values
y=data.iloc[ : ,0].values

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer()
cx=cv.fit_transform(x).todense()

##
###print(x,type(x))
##
from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest=train_test_split(cx,y,test_size=0.3,random_state=52)

from sklearn.naive_bayes import GaussianNB
model=GaussianNB()
model.fit(xtrain,ytrain)

ypred=model.predict(xtest)

from sklearn.metrics import accuracy_score
print(accuracy_score(ytest,ypred))