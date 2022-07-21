from storages.backends.s3boto3 import S3Boto3Storage

class static_storage(S3Boto3Storage):
    location = "static/"
    file_overwrite = False

class upload_storage(S3Boto3Storage):
    location = "uploads/"