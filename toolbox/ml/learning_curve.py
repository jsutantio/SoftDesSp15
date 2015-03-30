""" Exploring learning curves for classification of handwritten digits """

import matplotlib.pyplot as plt
import numpy
from sklearn.datasets import *
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

data = load_digits()
# print data.DESCR
num_trials = 500
train_percentages = range(5,90,5)
test_accuracies = numpy.zeros(len(train_percentages))
train_size = 0
train_list = []
test_list = []

for i in range(num_trials):
	for i in train_percentages:
		X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, train_size=i)
		model = LogisticRegression(C=1**-10)
		model.fit(X_train, y_train)
		train_list.append(model.score(X_train,y_train))
		test_list.append(model.score(X_test,y_test))
		# print "Train accuracy %f" %model.score(X_train,y_train)
		# print "Test accuracy %f"%model.score(X_test,y_test)
# print train_list
# print test_list

fig = plt.figure()
# plt.plot(train_list, test_list)
plt.plot(train_list, test_list, linewidth=0, marker='.')
plt.xlabel('Percentage of Data Used for Training')
plt.ylabel('Accuracy on Test Set')
plt.show()
