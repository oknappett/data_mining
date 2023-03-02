#load data
import json
with open('test_data.txt') as json_file:
    datpreda = json.load(json_file)

#create db
import pandas as pd
dfpred = pd.DataFrame(datpreda, columns = ['gmat', 'gpa', 'work_experience'])
Xpred = dfpred[['gmat', 'gpa']]
vars = ['gmat', 'gpa']

#load mdel from disk
import pickle
model_name = 'GMATgpa_regression.sav'
GMATgpa_model = pickle.load(open(model_name, 'rb'))

#predict
ypred = GMATgpa_model.predict(Xpred)
print(ypred)