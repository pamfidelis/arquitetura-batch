import boto3
import sys
import yaml
import logging
import os

sys.path.append('/home/pfidelis/Downloads/aws/arquitetura-batch-case')
from utils.sqs import SQSQueue
from utils.s3 import DataLake
from model.model import predict_model

# Load YAM
def load_yaml():
    with open('config/config.yaml') as file:
        return yaml.safe_load(file)

yaml_file = load_yaml()

# Load variables
bucket_name = yaml_file['aws_components']['s3']['name']

input_file_bucket = yaml_file['aws_components']['s3']['input_file']
input_file_local = os.path.join('data/input', input_file_bucket.split('/')[-1])

output_bucket = yaml_file['aws_components']['s3']['output_key']

model_file_bucket = yaml_file['aws_components']['s3']['model_file']

queue_name = yaml_file['aws_components']['sqs']

# call queue
queue = SQSQueue(queue_name)

# mock a message
queue.mock_send_message(bucket_name, input_file_bucket)
s3_bucket, s3_bucket_key = queue.receive_message()

s3 = DataLake(s3_bucket)

# download of the model
s3.download_file(model_file_bucket, model_file_bucket)

# download of file
s3.download_file(input_file_bucket, input_file_local)

output_path = predict_model(input_file_local, model_file_bucket)

output_bucket = os.path.join(output_bucket, output_path.split('/')[-1])

s3.upload_file(output_path, output_bucket)

queue.delete_message()
