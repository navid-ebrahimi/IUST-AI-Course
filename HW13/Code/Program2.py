from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train).predict(X_test)

correct_predictions = 0
for i in range(len(y_pred)):
  if y_pred[i] == y_test[i]:
      correct_predictions += 1
print("Accuracy: ", correct_predictions/len(y_pred) * 100, "%")

