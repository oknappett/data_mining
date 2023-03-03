import numpy as np

#import data set 
from sklearn import datasets
diabetes = datasets.load_diabetes()
cols = ['Age', 'Sex', 'BMI', 'Blood Pressure']
for i, col in enumerate(cols):
    x = diabetes.data[:,i]
    x = x[:, np.newaxis]
    y = diabetes.target

    #find the regression line
    from sklearn import linear_model
    linreg = linear_model.LinearRegression()
    linreg.fit(x, y)

    #plot the data
    import matplotlib.pyplot as plt
    plt.scatter(x, y, color='k')

    #draw fitted line
    ypred = linreg.predict(x)
    plt.plot(x, ypred, color='r', linewidth = 4)
    plt.xlabel("BMI")
    plt.ylabel("Disease indicator")

    plt.savefig("linreg_plots/diabetesRegression_%s.png"%(col))

    #pearsons correleation coefficiant
    from scipy.stats import pearsonr
    corr, _ = pearsonr(x.ravel(), y.ravel())
    print("Pearsons correlation coefficiant for %s: %.3f" %(col, corr))