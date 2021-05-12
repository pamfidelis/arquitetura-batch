from train_model import train_model
from sqs_queue import send_message
from config import load_config
import logging
import sys

sys.path.append('.')
from src.s3 import DataLake

def main(yaml_file):
    bucket_name = yaml_file['aws_components']['s3']['name']
    model_path = yaml_file['aws_components']['s3']['model_file']
    input_path = yaml_file['aws_components']['s3']['input_key']
    sqs_queue = yaml_file['aws_components']['sqs']

    s3_client = DataLake(bucket_name)

    train_model(model_path, input_path)

    s3_client.upload_file(input_path, input_path)    
    s3_client.upload_file(model_path, model_path)
    
    send_message(sqs_queue)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    yaml_file = load_config()
    
    main(yaml_file)