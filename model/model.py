import pickle
import pandas as pd
import os
import boto3

BUCKET = "arq-batch-s3"
dataset_path = os.path.abspath('../data/salary.csv')
model_local_path = os.path.abspath('../model/predicting_salaries.pkl')
score_path = os.path.abspath("../data/score.csv")

s3 = boto3.resource('s3')
s3.Bucket(BUCKET).download_file('salary.csv', dataset_path)
s3.Bucket(BUCKET).download_file('predicting_salaries.pkl', model_local_path)

ds = pd.read_csv('../data/salary.csv')
X = ds.iloc[:,:-1].values

modelo = pickle.load(open(model_local_path, 'rb'))
result = modelo.predict(X)

pd.DataFrame(result).to_csv(os.path.abspath(score_path))
s3.Bucket(BUCKET).upload_file(score_path, "score.csv")