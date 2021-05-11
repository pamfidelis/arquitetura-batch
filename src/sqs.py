import boto3
from botocore.exceptions import ClientError
import logging
import sys

logger = logging.getLogger(__name__)
# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='arq-batch-sqs')

def receive_messages(queue, max_number, wait_time):
    """
    Receive a batch of messages in a single request from an SQS queue.

    Usage is shown in usage_demo at the end of this module.

    :param queue: The queue from which to receive messages.
    :param max_number: The maximum number of messages to receive. The actual number
                       of messages received might be less.
    :param wait_time: The maximum time to wait (in seconds) before returning. When
                      this number is greater than zero, long polling is used. This
                      can result in reduced costs and fewer false empty responses.
    :return: The list of Message objects received. These each contain the body
             of the message and metadata and custom attributes.
    """
    try:
        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_time
        )
        for msg in messages:
            logger.info("Received message: %s: %s", msg.message_id, msg.body)
    except ClientError as error:
        logger.exception("Couldn't receive messages from queue: %s", queue)
        raise error
    else:
        return messages

while True:
    received_messages = receive_messages(queue, 1, 2)
    for message in received_messages:
        print(message.message_attributes['s3_bucket']['StringValue'])
        print(message.message_attributes['s3_bucket_key']['StringValue'])
        message.delete()
    if not received_messages:
        break
print('Done.')