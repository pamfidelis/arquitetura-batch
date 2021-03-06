from botocore.exceptions import ClientError
import logging
import boto3

logger = logging.getLogger(__name__)

class SQSQueue:
    """
    Class used to connect a Amazon SQS

    method availables:
    - mock_send_message: the purpose of this method is to simulate the reception of events coming from S3
    - receive_message: fetch messages in the queue


    :param queue_name: existing queue name into  AWS SQS

    """
    def __init__(self, queue_name):
        sqs = boto3.resource('sqs')
        self.queue = sqs.get_queue_by_name(QueueName=queue_name)


    def send_message(self):
        try:
            self.queue.send_message(MessageBody='s3_event', MessageAttributes={
                's3_bucket': {
                    'StringValue': "arq-batch-s3",
                    'DataType': 'String'
                },
                's3_bucket_file': {
                    'StringValue': "data/input/salary.csv",
                    'DataType': 'String'
                },
                's3_bucket_model': {
                    'StringValue': "model/predicting_salaries.pkl",
                    'DataType': 'String'
                }
            })
        except ClientError as error:
            logger.exception(f"Couldn't not send the message from the queue: {self.queue}")
            raise error


    def receive_message(self):
        try:
            messages = self.queue.receive_messages(
                MessageAttributeNames=['All'],
                MaxNumberOfMessages=1,
            )

            for msg in messages:
                self.message = msg
            s3_bucket = self.message.message_attributes['s3_bucket']['StringValue']
            s3_bucket_file = self.message.message_attributes['s3_bucket_file']['StringValue']
            s3_bucket_model = self.message.message_attributes['s3_bucket_model']['StringValue']


        except ClientError as error:
            logger.exception(f"Couldn't receive messages from queue: {self.queue}")
            raise error
        else:
            return s3_bucket, s3_bucket_file, s3_bucket_model


    def delete_message(self):
        self.message.delete()
