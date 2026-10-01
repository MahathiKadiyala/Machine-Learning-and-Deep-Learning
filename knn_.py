
import pandas as pd
import sklearn
df=pd.read_csv(r"C:\Users\mahat\Downloads\iris.csv")
#print(df)

#df.shape
 
#df.columns

#print(df.info)

x=df.iloc[: , :-1]
y=df.iloc[: , -1]


from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=2)

from sklearn.neighbors import KNeighborsClassifier
model=KNeighborsClassifier(n_neighbors=2)
model.fit(xtrain,ytrain)

ypred=model.predict(xtest)

from sklearn.metrics import accuracy_score
print(accuracy_score(ytest,ypred)*100)

print(model.predict([[1.2,2.3,4.2,0.8]]))
