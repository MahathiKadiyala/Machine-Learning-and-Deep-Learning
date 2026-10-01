import pandas as  pd
data=pd.read_csv(r"C:\Users\mahat\Downloads\iris.csv")

##print(data.head)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data['class'] = le.fit_transform(data['class'])

from sklearn.cluster import KMeans
model=KMeans(n_clusters=3)

model.fit(data)
x=model.predict(data)

data['prediction']=x
data.to_csv(r'C:\Users\mahat\OneDrive\Desktop\Machine_learning\kmeans_prediction.csv')


