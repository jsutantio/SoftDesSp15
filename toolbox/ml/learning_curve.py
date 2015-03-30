""" Exploring learning curves for classification of handwritten digits """

import matplotlib.pyplot as plt
import numpy
from sklearn.datasets import *
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

data = load_digits()
# print data.DESCR
num_trials = 10
train_percentages = range(5,90,5)
test_accuracies = numpy.zeros(len(train_percentages))

train_size = 0.5

for i in range(num_trials):
	for i in train_percentages:
		X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, train_size=i)
		model = LogisticRegression(C=10**-10)
		model.fit(X_train, y_train)
		print "Train accuracy %f" %model.score(X_train,y_train)
		print "Test accuracy %f"%model.score(X_test,y_test)

fig = plt.figure()
plt.plot(model.score(X_train,y_train), model.score(X_test,y_test))
plt.xlabel('Percentage of Data Used for Training')
plt.ylabel('Accuracy on Test Set')
plt.show()
