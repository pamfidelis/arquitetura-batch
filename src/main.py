import boto3
import sys
import yaml
import logging

sys.path.append('/home/pfidelis/Downloads/aws/arquitetura-batch-case')
from utils.sqs import SQSQueue

def load_yaml():
    with open('config/config.yaml') as file:
        return yaml.safe_load(file)

yaml_file = load_yaml()

bucket_name = yaml_file['aws_components']['s3']['bucket']
bucket_key = yaml_file['aws_components']['s3']['bucket_input']
queue_name = yaml_file['aws_components']['sqs']

queue = SQSQueue(queue_name)

queue.mock_send_message(bucket_name, bucket_key)
s3_bucket, s3_bucket_key = queue.receive_message()

print(s3_bucket)
print(s3_bucket_key)

queue.delete_message()
