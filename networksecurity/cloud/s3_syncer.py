# NETWORKSECURITY/networksecurity/cloud/s3_syncer.py

import os
import sys
import boto3
from botocore.exceptions import ClientError

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class S3Sync:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def _parse_s3_url(self,aws_bucket_url: str):
        """s3://bucket-name/prefix 파싱"""
        path = aws_bucket_url.replace("s3://", "")
        parts = path.split("/", 1)
        bucket = parts[0]
        prefix = parts[1].rstrip("/") if len(parts) > 1 else ""
        return bucket, prefix

    def _s3_path_exists(self,bucket: str,prefix: str) -> bool:
        """S3 경로(prefix) 존재 여부 확인"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=bucket, Prefix=prefix, MaxKeys=1
            )
            return response.get("KeyCount", 0) > 0
        except ClientError as e:
            logging.warning(f"S3 path check failed: {e}")
            return False

    def sync_folder_to_s3(self,folder: str,aws_bucket_url: str):
        try:
            if not os.path.exists(folder):
                logging.warning(f"Folder {folder} does not exist") # AWS 컨테이내 로그 확인
                return

            bucket, prefix = self._parse_s3_url(aws_bucket_url)

            for root, _, files in os.walk(folder):
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, folder)
                    s3_key = os.path.join(prefix, relative_path).replace("\\", "/")

                    self.s3_client.upload_file(local_path, bucket, s3_key)
                    logging.info(f"Uploaded: {local_path} -> s3://{bucket}/{s3_key}")

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        try:
            bucket, prefix = self._parse_s3_url(aws_bucket_url)

            if not self._s3_path_exists(bucket, prefix):
                logging.warning(f"S3 path {aws_bucket_url} does not exist")
                return

            os.makedirs(folder, exist_ok=True)

            paginator = self.s3_client.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
                for obj in page.get("Contents", []):
                    s3_key = obj["Key"]
                    relative_path = os.path.relpath(s3_key, prefix)
                    local_path = os.path.join(folder, relative_path)

                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    self.s3_client.download_file(bucket, s3_key, local_path)
                    logging.info(f"Downloaded: s3://{bucket}/{s3_key} -> {local_path}")

        except Exception as e:
            raise NetworkSecurityException(e,sys)