import logging.config
import yaml
import sys
import os

sys.path.append('.')
from utils.sqs import SQSQueue
from utils.s3 import DataLake
from model.model import predict_model


logging.basicConfig(filename='arq_batch.log',
                format='%(levelname)s %(asctime)s :: %(message)s',
                level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load_config():
    try:
        with open('config/config.yaml') as file:
            return yaml.safe_load(file)
    except IOError as e:
            logger.exception(f"I/O error({e.errno}): {e.strerror}")
            raise e
    except: 
        logger.exception(f"Unexpected error: {sys.exc_info()[0]}")


def execute_model(s3_bucket, file_input_bucket, model_path_bucket, file_output_bucket):
    """
    Download the model pickle and input files from S3, make the prediction and upload the output to S3

    :param s3_bucket: Bucket name
    :param file_input_bucket: file input path from S3
    :param model_path_bucket: pickle model path from S3
    :param file_output_bucket: file output path into S3

    :return: None
    """

    model_path_local = os.path.join('model', model_path_bucket.split('/')[-1])
    input_path_local = os.path.join('data/input', file_input_bucket.split('/')[-1])
    output_path_local = os.path.abspath('data/output/score.csv')

    s3_client = DataLake(s3_bucket)

    s3_client.download_file(model_path_bucket, model_path_local)
    s3_client.download_file(file_input_bucket, input_path_local)
    
    predict_model(input_path_local, model_path_local, output_path_local)

    s3_client.upload_file(output_path_local, file_output_bucket)


def main(yaml_file):
    file_output_bucket = yaml_file['aws_components']['s3']['output_key']
    sqs_queue = yaml_file['aws_components']['sqs']

    queue = SQSQueue(sqs_queue)
    queue.mock_send_message()

    s3_bucket, file_input_bucket, model_path_bucket = queue.receive_message()
   
    execute_model(s3_bucket, file_input_bucket, model_path_bucket, file_output_bucket)

    queue.delete_message()

if __name__ == "__main__":
    yaml_file = load_config()

    main(yaml_file)
