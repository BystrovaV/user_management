from botocore.client import BaseClient
from fastapi import Depends

from adapters.localstack.localstack import LocalStack
from core.settings import Settings, get_settings


class LocalStackDependency:
    def __init__(self):
        self.localstack = None

    async def __call__(self, settings: Settings = Depends(get_settings)) -> LocalStack:
        self.localstack = (
            await LocalStack.start(settings) if not self.localstack else self.localstack
        )
        return self.localstack


get_localstack_dependency = LocalStackDependency()


async def get_localstack_s3_client(
    localstack: LocalStack = Depends(get_localstack_dependency),
    settings: Settings = Depends(get_settings),
) -> BaseClient:
    async with localstack.session.client(
        "s3", endpoint_url=settings.get_localstack_endpoint()
    ) as client:
        yield client


async def get_localstack_ses_client(
    localstack: LocalStack = Depends(get_localstack_dependency),
    settings: Settings = Depends(get_settings),
) -> BaseClient:
    async with localstack.session.client(
        "ses", endpoint_url=settings.get_localstack_endpoint()
    ) as client:
        yield client
