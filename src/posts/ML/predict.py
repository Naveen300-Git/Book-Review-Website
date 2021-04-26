from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import RidgeCV
import numpy as np
import pandas as pd
import pickle
import os

def calc_expertivity(a,b):
	path = os.getcwd()
	loaded_model=pickle.load(open(os.path.join(path,'posts/ML/model.h5'),'rb'))
	sc=pickle.load(open(os.path.join(path,'posts/ML/std_scaler.bin'),'rb'))
#let input tuple be k(follower count, total no of upvotes)
	k=[[a,b]]
	k=sc.transform(k)
	Ypred=loaded_model.predict(k)

	return Ypred #GIVES THE EXPERTISE
