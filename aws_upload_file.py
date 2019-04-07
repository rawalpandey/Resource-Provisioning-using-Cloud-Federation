import boto3
from botocore.client import Config

ACCESS_KEY_ID = '*************'
ACCESS_SECRET_KEY = '***************'
BUCKET_NAME = '*************'
FILE_NAME = 'hello1.txt';


data = open(FILE_NAME, 'rb')

# S3 Connect

s3 = boto3.client('s3')
s3.create_bucket(Bucket = BUCKET_NAME)
s3.upload_file(FILE_NAME,BUCKET_NAME, FILE_NAME)
s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)


s3.Bucket(BUCKET_NAME).download_file(FILE_NAME, './abc'); 
