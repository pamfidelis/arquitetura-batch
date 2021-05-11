from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle
import boto3
import os

s3 = boto3.resource('s3')
BUCKET = "arq-batch-s3"

dataset_path = os.path.abspath('../data/salary.csv')

s3.Bucket(BUCKET).download_file('salary.csv', dataset_path)
ds = pd.read_csv(os.path.abspath(dataset_path))

#importing dataset and declaring independent and dependent variable
#the dependent variable is in last column, hence y is assigned with [:,-1] (meaning all rows of last column)
x = ds.iloc[:,:-1].values
y = ds.iloc[:,-1].values

#splitting dataset in training and testing set
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2, random_state = 0)

#training the model
lr = LinearRegression()
lr.fit(x_train,y_train)

# generate pickle of a model
model_local_path = os.path.abspath('../model/predicting_salaries.pkl')
pickle.dump(lr, open(model_local_path, 'wb'))

s3.Bucket(BUCKET).upload_file(model_local_path, "predicting_salaries.pkl")