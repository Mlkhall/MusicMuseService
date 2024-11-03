from music_muse.settings import (
    S3_STATIC_LOCATION,
    S3_PUBLIC_MEDIA_LOCATION,
    S3_PRIVATE_MEDIA_LOCATION,
)
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = S3_STATIC_LOCATION
    file_overwrite = True
    default_acl = "public-read"


class PublicMediaStorage(S3Boto3Storage):
    location = S3_PUBLIC_MEDIA_LOCATION
    file_overwrite = True
    default_acl = "public-read"


class PrivateMediaStorage(S3Boto3Storage):
    location = S3_PRIVATE_MEDIA_LOCATION
    default_acl = "private"
    file_overwrite = False
    custom_domain = False
