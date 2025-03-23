"""
AWS S3 서비스 접근 모듈
"""
import logging
from typing import List, Optional

import boto3
from botocore.exceptions import ClientError

# 로깅 설정
logger = logging.getLogger(__name__)


class S3Client:
    """
    AWS S3 버킷에 접근하고 파일을 관리하는 클래스
    """

    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        region_name: str = "ap-northeast-2",
    ):
        """
        S3 클라이언트 초기화

        Args:
            aws_access_key_id: AWS 액세스 키 ID
            aws_secret_access_key: AWS 시크릿 액세스 키
            region_name: AWS 리전 이름 (기본값: 서울)
        """
        if aws_access_key_id is None or aws_secret_access_key is None:
            logger.error("AWS 인증 정보가 없습니다.")
            raise ValueError("AWS 인증 정보가 없습니다.")

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

        self.s3_resource = boto3.resource(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def list_buckets(self) -> List[str]:
        """
        사용 가능한 S3 버킷 목록 조회

        Returns:
            List[str]: 버킷 이름 목록
        """
        try:
            response = self.s3_client.list_buckets()
            return [bucket["Name"] for bucket in response["Buckets"]]
        except ClientError as e:
            logger.error("S3 버킷 목록 조회 실패: %s", str(e))
            raise

    def upload_file(
        self, file_path: str, bucket_name: str, object_name: Optional[str] = None
    ) -> bool:
        """
        파일을 S3 버킷에 업로드

        Args:
            file_path: 업로드할 로컬 파일 경로
            bucket_name: 대상 버킷 이름
            object_name: S3에 저장될 객체 이름 (기본값: 파일 이름 그대로 사용)

        Returns:
            bool: 업로드 성공 여부
        """
        if object_name is None:
            object_name = file_path.split("/")[-1]

        try:
            self.s3_client.upload_file(file_path, bucket_name, object_name)
            logger.info(
                "파일 업로드 성공: %s -> %s/%s", file_path, bucket_name, object_name
            )
            return True
        except ClientError as e:
            logger.error("파일 업로드 실패: %s", str(e))
            return False

    def download_file(self, bucket_name: str, object_name: str, file_path: str) -> bool:
        """
        S3 버킷에서 파일 다운로드

        Args:
            bucket_name: 소스 버킷 이름
            object_name: 다운로드할 S3 객체 이름
            file_path: 저장할 로컬 파일 경로

        Returns:
            bool: 다운로드 성공 여부
        """
        try:
            self.s3_client.download_file(bucket_name, object_name, file_path)
            logger.info(
                "파일 다운로드 성공: %s/%s -> %s", bucket_name, object_name, file_path
            )
            return True
        except ClientError as e:
            logger.error("파일 다운로드 실패: %s", str(e))
            return False

    def list_objects(self, bucket_name: str, prefix: str = "") -> List[str]:
        """
        S3 버킷 내 객체 목록 조회

        Args:
            bucket_name: 버킷 이름
            prefix: 객체 접두사 (폴더 경로)

        Returns:
            List[str]: 객체 키 목록
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

            if "Contents" not in response:
                return []

            return [obj["Key"] for obj in response["Contents"]]
        except ClientError as e:
            logger.error("객체 목록 조회 실패: %s", str(e))
            raise

    def delete_object(self, bucket_name: str, object_name: str) -> bool:
        """
        S3 버킷에서 객체 삭제

        Args:
            bucket_name: 버킷 이름
            object_name: 삭제할 객체 이름

        Returns:
            bool: 삭제 성공 여부
        """
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=object_name)
            logger.info("객체 삭제 성공: %s/%s", bucket_name, object_name)
            return True
        except ClientError as e:
            logger.error("객체 삭제 실패: %s", str(e))
            return False
