import tempfile
import uuid
from typing import BinaryIO

import aioboto3
from aiohttp import web
from botocore.client import BaseClient
from botocore.exceptions import ClientError, NoCredentialsError
from multidict import MultiDict

from core.exceptions import LocalStackConnectionException
from core.settings import Settings
from ports.repositories.email_service import EmailService
from ports.repositories.image_repository import ImageRepository


class LocalStack:
    def __init__(self, session):
        self.session = session

    @classmethod
    async def start(cls):
        settings = Settings()
        session = aioboto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name="us-east-1",
        )

        async with session.client(
            "s3",
            endpoint_url=settings.get_localstack_endpoint(),
        ) as client:
            print(settings.BUCKET_NAME)
            try:
                await client.head_bucket(Bucket=settings.BUCKET_NAME)
            except ClientError:
                await client.create_bucket(Bucket=settings.BUCKET_NAME)

        return cls(session)


class LocalStackS3Repository(ImageRepository):
    def __init__(self, client: BaseClient):
        self.client = client

    async def upload_image(self, file: BinaryIO, filename: str) -> str:
        settings = Settings()
        try:
            random_file_name = "".join([str(uuid.uuid4().hex[:6]), filename])
            await self.client.upload_fileobj(
                file, settings.BUCKET_NAME, random_file_name
            )
            return settings.get_image_url(random_file_name)
        except Exception:
            raise LocalStackConnectionException


class LocalStackSESService(EmailService):
    def __init__(self, client: BaseClient):
        self.client = client

    async def send_email(self, email: str, text: str):
        try:
            await self.client.verify_email_identity(
                EmailAddress="user_management@example.org"
            )
            print(f"Email {email} успешно верифицирован.")
        except NoCredentialsError:
            print("Ошибка: Учетные данные не найдены.")
        except Exception as e:
            print(f"Ошибка при верификации email-адреса: {str(e)}")

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
            raise LocalStackConnectionException
