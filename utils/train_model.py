from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import logging
import pickle
import sys

sys.path.append('.')
from utils.config import load_config
from src.s3 import DataLake


def train_model(model_path, input_path):  
    # Read dataset
    df = pd.read_csv(input_path)

    #importing dataset and declaring independent and dependent variable
    #the dependent variable is in last column, hence y is assigned with [:,-1] (meaning all rows of last column)
    x = df.iloc[:,:-1].values
    y = df.iloc[:,-1].values

    #splitting dataset in training and testing set
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2, random_state = 0)

    #training the model
    lr = LinearRegression()
    lr.fit(x_train,y_train)

    # generate pickle of a model
    pickle.dump(lr, open(model_path, 'wb'))
    
