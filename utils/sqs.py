from botocore.exceptions import ClientError
import logging
import boto3

logger = logging.getLogger(__name__)

class SQSQueue:
    def __init__(cls, queue_name):
        sqs = boto3.resource('sqs')
        cls.queue = sqs.get_queue_by_name(QueueName=queue_name)


    def mock_send_message(cls, s3_bucket, s3_bucket_file):
        try:
            cls.queue.send_message(MessageBody='s3_event', MessageAttributes={
                's3_bucket': {
                    'StringValue': s3_bucket,
                    'DataType': 'String'
                },
                's3_bucket_file': {
                    'StringValue': s3_bucket_file,
                    'DataType': 'String'
                }
            })
        except ClientError as error:
            logger.exception(f"Couldn't not send the message from the queue: {cls.queue}")
            raise error


    def receive_message(cls):
        try:
            messages = cls.queue.receive_messages(
                MessageAttributeNames=['All'],
                MaxNumberOfMessages=1,
            )
            
            cls.message = messages[0]
            s3_bucket = cls.message.message_attributes['s3_bucket']['StringValue']
            s3_bucket_key = cls.message.message_attributes['s3_bucket_file']['StringValue']
            

        except ClientError as error:
            logger.exception(f"Couldn't receive messages from queue: {cls.queue}")
            raise error
        else:
            return s3_bucket, s3_bucket_key


    def delete_message(cls):
        cls.message.delete()
