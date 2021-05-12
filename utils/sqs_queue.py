import sys

sys.path.append('.')
from src.sqs import SQSQueue

def send_message(sqs_queue):
    queue = SQSQueue(sqs_queue)
    queue.send_message()