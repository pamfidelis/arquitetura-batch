import pickle
import pandas as pd
import os
import boto3

def predict_model(input_path, model_path):
    output_path = os.path.abspath('data/output/score.csv')
    
    ds = pd.read_csv(input_path)
    X = ds.iloc[:,:-1].values

    modelo = pickle.load(open(model_path, 'rb'))
    result = modelo.predict(X)

    pd.DataFrame(result).to_csv(output_path)

    return output_path
