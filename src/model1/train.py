'''
Gradient Boosted Decision Tree
Features: data/users1.csv + data/book_basic_encode.csv (all features)
Samples: original_data/books_ratings_train.csv
Data: model1/train.dat
'''

import sys
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split

def MAE(pred, label):
    pred = np.rint(pred)
    return np.average(np.abs(label-pred))

def MAPE(pred, label):
    pred = np.rint(pred)
    return np.average(np.abs((label-pred)/label)) * 100

train_file = sys.argv[1]
test_file = sys.argv[2]
submission_file = sys.argv[3]

n_feature = 8

data = np.fromfile(train_file, sep=' ')
data = np.reshape(data, (data.size//(n_feature+1), n_feature+1))

Xtest = np.fromfile(test_file, sep=' ')
Xtest = np.reshape(Xtest, (Xtest.size//n_feature, n_feature))

Xtrain, Xval, Ytrain, Yval = train_test_split(data[:,:-1], data[:,-1], test_size=0.2, random_state=1126)

clf = xgb.XGBRegressor(max_depth=50, learning_rate=0.3, n_estimators=100, objective='reg:linear', gamma=100, reg_lambda=1, n_jobs=8, silent=False)
clf.fit(Xtrain, Ytrain, early_stopping_rounds=50, eval_set=[(Xval, Yval)])
pred_train = clf.predict(Xtrain)
pred_val = clf.predict(Xval)

print('Train MAE: {}'.format(MAE(pred_train, Ytrain)))
print('Train MAPE: {}'.format(MAPE(pred_train, Ytrain)))
print('Validation MAE: {}'.format(MAE(pred_val, Yval)))
print('Validation MAPE: {}'.format(MAPE(pred_val, Yval)))

test_pred = clf.predict(Xtest)
test_pred = np.rint(test_pred).astype(int)
np.savetxt(submission_file, test_pred, fmt='%i')