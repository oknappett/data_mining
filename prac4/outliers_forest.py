import numpy as np

#load data
from sklearn import datasets
diabetes = datasets.load_diabetes()
x = diabetes.data[:,3]
x = x[:,np.newaxis]
y = diabetes.target

# Add some irrelevant data/outliers to x using random numbers.
# The amplitude of outliers are in [-2.5,2.5]. We just add outliers to
# 10 numbers of x in random way
outlier_index = np.random.randint(x.shape[0], size=10) # create random indices
x[outlier_index,0] = 2.5*np.random.rand((10)) # distribute outliers over 10 values of x

#isolation forest return the indices of calid values
from sklearn.ensemble import IsolationForest
clf = IsolationForest(max_samples=10000, random_state = 1, contamination ='auto')
index = clf.fit_predict(x)

#using forest, keep valid values
print("before applying IsolationForest: ", len(x))
x = x[index==1]
y = y[index==1]
print("after applying IsolationForest: ", len(x))

# find the line fitting to (x,y)
from sklearn import linear_model
model = linear_model.LogisticRegression(solver='liblinear')
Line = model.fit(x,y)
# calculate Pearson's correlation
from scipy.stats import pearsonr
corr, _ = pearsonr(x.ravel(), y.ravel())
print('Pearsons correlation: %.3f' % corr)