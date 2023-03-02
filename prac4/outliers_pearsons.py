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

#remove outliers now
import scipy.signal
kernel_size = 9
x = scipy.signal.medfilt(x.ravel(), kernel_size)
x = x[:,np.newaxis]

#find line to fit x,y
from sklearn import linear_model
model = linear_model.LogisticRegression(solver = 'liblinear')
line = model.fit(x,y)

#calculate pearson's corellation
from scipy.stats import pearsonr
corr, _ = pearsonr(x.ravel(),y.ravel())
print('Pearsons correlation: %.3f' % corr)