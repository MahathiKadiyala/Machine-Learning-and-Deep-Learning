#Decision Tree
import pandas as pd

data = pd.read_csv(r"C:\Users\mahat\Downloads\spam.csv", encoding = "latin-1")
x = data["v2"].to_numpy()
y = data["v1"].to_numpy()

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
cx = cv.fit_transform(x).toarray()

from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(cx, y, test_size = 0.2, random_state = 2)

from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()   # By default it will take Gini Index
#model = DecisionTreeClassifier(criterion = 'entropy')
model.fit(xtrain, ytrain)
ypred = model.predict(xtest)

from sklearn.metrics import accuracy_score
print(accuracy_score(ytest, ypred))
