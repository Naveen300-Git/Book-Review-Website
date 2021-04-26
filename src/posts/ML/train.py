import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import RidgeCV
import joblib
import matplotlib.pyplot as plt

data=pd.read_csv("data.csv")
columns=['follower_count','gender','sum(voteup_count)']
for col in columns:
  data[col]=data[col].astype(float)

data=data.drop(['name','gender'], axis = 1)
X=data.iloc[:,0:-1].values
Y=data.iloc[:,-1].values
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=42)
sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.fit_transform(X_test)
model = LinearRegression()
#model=RidgeCV()
model.fit(X_train,Y_train)
pickle.dump(model,open('model.h5','wb'))
pickle.dump(sc, open('std_scaler.bin','wb'))