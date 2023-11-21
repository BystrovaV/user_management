import aioboto3
from aioboto3 import Session
from botocore.client import BaseClient
from fastapi import Depends

from adapters.localstack.localstack import LocalStack
from core.settings import Settings


class LocalStackDependency:
    def __init__(self):
        self.localstack = None

    async def __call__(self) -> LocalStack:
        self.localstack = (
            await LocalStack.start() if not self.localstack else self.localstack
        )
        return self.localstack


get_localstack_dependency = LocalStackDependency()


async def get_localstack_s3_client(
    localstack: LocalStack = Depends(get_localstack_dependency),
) -> BaseClient:
    settings = Settings()
    async with localstack.session.client(
        "s3", endpoint_url=settings.get_localstack_endpoint()
    ) as client:
        yield client


async def get_localstack_ses_client(
    localstack: LocalStack = Depends(get_localstack_dependency),
) -> BaseClient:
    settings = Settings()
    async with localstack.session.client(
        "ses", endpoint_url=settings.get_localstack_endpoint()
    ) as client:
        yield client
