import logging.config
import yaml
import sys
import os
from sqs import SQSQueue
from s3 import DataLake

sys.path.append('.')
from utils.config import load_config
from model.model import predict_model


logging.basicConfig(filename='arq_batch.log',
                format='%(levelname)s %(asctime)s :: %(message)s',
                level=logging.DEBUG)


def execute_model(s3_bucket, file_input, model_path, file_output):
    """
    Download the model pickle and input files from S3, make the prediction and upload the output to S3

    :param s3_bucket: Bucket name
    :param file_input: file input path from S3
    :param model_path: pickle model path from S3
    :param file_output: file output path into S3

    :return: None
    """

    s3_client = DataLake(s3_bucket)
    s3_client.download_file(model_path, model_path)

    s3_client.download_file(file_input, file_input)
    
    predict_model(file_input, model_path, file_output)

    s3_client.upload_file(file_output, file_output)


def main(yaml_file):
    file_output = yaml_file['aws_components']['s3']['output_key']
    file_input = yaml_file['aws_components']['s3']['input_key']
    sqs_queue = yaml_file['aws_components']['sqs']

    queue = SQSQueue(sqs_queue)
    s3_bucket, file_input, model_path = queue.receive_message()
   
    execute_model(s3_bucket, file_input, model_path, file_output)

    queue.delete_message()

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    yaml_file = load_config()

    main(yaml_file)
