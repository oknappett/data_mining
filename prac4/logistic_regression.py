#load data
import json
with open("Data_Reg.txt") as json_file:
    candidates = json.load(json_file)

#create db
import pandas as pd
df = pd.DataFrame(candidates, columns=['gmat', 'gpa', 'work_experience', 'admitted'])

X = df[['gmat', 'gpa', 'work_experience']]
Y = df['admitted']

#define independent and dependent variables
vars = ['gmat', 'gpa']
x = df[vars]
y = Y

# find erlationship between parameters using logistic regression
from sklearn.linear_model import LogisticRegression
logis_reg = LogisticRegression(solver='lbfgs').fit(x, y.values.ravel())

#estimate params
print('Intercept = %f' % (logis_reg.intercept_))
print('Slope = ', logis_reg.coef_[0,:], logis_reg.intercept_)

# save the model to disk
import pickle
filename = 'GMATgpa_regression.sav'
pickle.dump(logis_reg, open(filename, 'wb'))

import matplotlib.pyplot as plt
x_gmat = df[vars[0]]
x_gpa = df[vars[1]]
fig = plt.figure()
Admitted_index = Y == 1

plt.scatter(x_gmat[Admitted_index], x_gpa[Admitted_index],c='red',label="Admitted")
Rejected_index=~Admitted_index # or Admitted_index = Y == 0
plt.scatter(x_gmat[Rejected_index], x_gpa[Rejected_index],c='blue',label="Rejected")
# draw the Fitted Line
import numpy as np
h = .02 # step size in the mesh
x_min, x_max = x_gmat.min() - 1, x_gmat.max() + 1
y_min, y_max = x_gpa.min() - 1, x_gpa.max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),np.arange(y_min, y_max, h))
Line = logis_reg.predict(np.c_[xx.ravel(), yy.ravel()])
plt.contour(xx, yy, Line.reshape(xx.shape), 10, colors='k')
plt.xlabel("gmat")
plt.ylabel("gpa")
plt.legend(loc='upper left')
plt.savefig('logreg_plots/logreg_gpavsexp.png')
