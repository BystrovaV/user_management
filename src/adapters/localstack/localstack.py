import logging
import uuid
from typing import BinaryIO

import aioboto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError, NoCredentialsError

from core.exceptions import LocalStackConnectionException
from core.settings import Settings
from ports.repositories.email_service import EmailService
from ports.repositories.image_repository import ImageRepository

logger = logging.getLogger(__name__)


class LocalStack:
    def __init__(self, session):
        self.session = session

    @classmethod
    async def start(cls, settings: Settings):
        session = aioboto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name="us-east-1",
        )

        async with session.client(
            "s3",
            endpoint_url=settings.get_localstack_endpoint(),
        ) as client:
            try:
                await client.head_bucket(Bucket=settings.BUCKET_NAME)
                logger.info("Bucket is created")
            except ClientError:
                logger.info("Bucket is not found. Create a new one")
                await client.create_bucket(Bucket=settings.BUCKET_NAME)

        return cls(session)


class LocalStackS3Repository(ImageRepository):
    def __init__(self, client: BaseClient, settings: Settings):
        self.client = client
        self.settings = settings

    async def upload_image(self, file: BinaryIO, filename: str) -> str:
        try:
            random_file_name = "".join([str(uuid.uuid4().hex[:6]), filename])
            await self.client.upload_fileobj(
                file, self.settings.BUCKET_NAME, random_file_name
            )
            return self.settings.get_image_url(random_file_name)
        except Exception as e:
            logger.exception(e)
            raise LocalStackConnectionException


class LocalStackSESService(EmailService):
    def __init__(self, client: BaseClient):
        self.client = client

    async def send_email(self, email: str, text: str):
        try:
            await self.client.verify_email_identity(
                EmailAddress="user_management@example.org"
            )
            logger.info(f"Email {email} is successfully verifyied")
        except NoCredentialsError as e:
            logger.exception(e)
            raise LocalStackConnectionException
        except Exception as e:
            logger.exception(e)
            raise LocalStackConnectionException

        try:
            await self.client.send_email(
                Destination={
                    "ToAddresses": [
                        email,
                    ],
                },
                Message={
                    "Body": {
                        "Text": {
                            "Charset": "UTF-8",
                            "Data": text,
                        }
                    },
                    "Subject": {
                        "Charset": "UTF-8",
                        "Data": text,
                    },
                },
                Source="user_management@example.org",
            )
        except Exception:
            logger.exception(e)
            raise LocalStackConnectionException
