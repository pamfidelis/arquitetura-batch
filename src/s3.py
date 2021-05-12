from botocore.exceptions import ClientError
import logging
import boto3

logger = logging.getLogger(__name__)

class DataLake:
    """
    Class used to connect a Amazon S3

    params: bucket_name 
    """

    def __init__(self, bucket_name):        
        s3_client = boto3.resource('s3')
        self.bucket = s3_client.Bucket(bucket_name)

    
    def download_file(self, source, target):
        """
        Download file from S3

        :param source: S3 bucket/file
        :param target: local path/name 

        :return: None
        """

        try:
            self.bucket.download_file(source, target)


        except ClientError as error:
            logger.exception(f"Couldn't download file from S3")
            raise error


    def upload_file(self, source, target):
        """
        Upload file from S3

        :param source: local path/name 
        :param target: S3 bucket/file

        :return: None
        """

        try:
           self.bucket.upload_file(source, target)
            
        except ClientError as error:
            logger.exception(f"Couldn't upload file to S3")
            logger.exception(error)
            raise error
