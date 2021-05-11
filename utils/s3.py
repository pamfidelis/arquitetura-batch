from botocore.exceptions import ClientError
import logging
import boto3

logger = logging.getLogger(__name__)

class DataLake():
    def __init__(cls, bucket_name):        
        s3 = boto3.resource('s3')
        cls.bucket = s3.Bucket(bucket_name)

    
    def download_file(cls, source, target):
        try:
            cls.bucket.download_file(source, target)


        except ClientError as error:
            logger.exception(f"Couldn't download file from S3")
            raise error
    

    def upload_file(cls, source, target):
        try:
           cls.bucket.upload_file(source, target)
            
        except ClientError as error:
            logger.exception(f"Couldn't upload file to S3")
            logger.exception(error)
            raise error
