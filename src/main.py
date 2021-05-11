import boto3
import sys
import yaml
import logging
import os

sys.path.append('/home/pfidelis/Downloads/aws/arquitetura-batch-case')
from utils.sqs import SQSQueue
from utils.s3 import DataLake

def load_yaml():
    with open('config/config.yaml') as file:
        return yaml.safe_load(file)

yaml_file = load_yaml()

bucket_name = yaml_file['aws_components']['s3']['name']

bucket_input = yaml_file['aws_components']['s3']['input']['key']
bucket_input_file = yaml_file['aws_components']['s3']['input']['file']

bucket_output = yaml_file['aws_components']['s3']['output']['key']

bucket_model = yaml_file['aws_components']['s3']['model']['key']
bucket_model_file = yaml_file['aws_components']['s3']['model']['file']

queue_name = yaml_file['aws_components']['sqs']


queue = SQSQueue(queue_name)

queue.mock_send_message(bucket_name, bucket_input)
s3_bucket, s3_bucket_key = queue.receive_message()

s3 = DataLake(s3_bucket)

s3_model_file = bucket_model + '/' + bucket_model_file
model_path_local = os.path.join('model', bucket_model_file)

print(s3_model_file)

s3.download_file(s3_model_file, model_path_local)

queue.delete_message()
