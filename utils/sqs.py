from botocore.exceptions import ClientError
import logging
import boto3

logger = logging.getLogger(__name__)

class SQSQueue:
    def __init__(self, queue_name):
        sqs = boto3.resource('sqs')
        self.queue = sqs.get_queue_by_name(QueueName=queue_name)


    def mock_send_message(self):
        try:
            self.queue.send_message(MessageBody='s3_event', MessageAttributes={
                's3_bucket': {
                    'StringValue': "arq-batch-s3",
                    'DataType': 'String'
                },
                's3_bucket_file': {
                    'StringValue': "input/salary.csv",
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
            
            self.message = messages[0]
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
