from decouple import config
from storages.backends.s3boto3 import S3Boto3Storage

AWS_STORAGE_BUCKET_NAME_STATIC = config("AWS_STORAGE_BUCKET_NAME_STATIC")
AWS_STORAGE_BUCKET_NAME_MEDIA = config("AWS_STORAGE_BUCKET_NAME_MEDIA")

class CustomS3StaticStorage(S3Boto3Storage):
    bucket_name = AWS_STORAGE_BUCKET_NAME_STATIC

class CustomS3MediaStorage(S3Boto3Storage):
    bucket_name = AWS_STORAGE_BUCKET_NAME_MEDIA