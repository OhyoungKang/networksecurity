# NETWORKSECURITY/networksecurity/cloud/s3_syncer.py

import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class S3Sync:
    def sync_folder_to_s3(self,folder,aws_bucket_url):
        try:
            command = f"aws s3 sync {folder} {aws_bucket_url}"
            rc = os.system(command)
            if rc != 0:
                raise Exception("Error while syncing folder to s3 bucket")

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        try:
            command = f"aws s3 sync {aws_bucket_url} {folder}"
            rc = os.system(command)
            if rc != 0:
                raise Exception("Error while syncing folder from s3 bucket")

        except Exception as e:
            raise NetworkSecurityException(e,sys)