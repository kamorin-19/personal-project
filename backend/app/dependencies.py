from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

import aioboto3
from aioboto3 import Session

from app.config import settings

if TYPE_CHECKING:
    from types_aiobotocore_dynamodb import DynamoDBServiceResource


_session: Session = aioboto3.Session()


async def get_dynamodb() -> AsyncGenerator["DynamoDBServiceResource", None]:
    async with _session.resource(
        "dynamodb",
        endpoint_url=settings.dynamodb_endpoint_url,
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    ) as dynamodb:
        yield dynamodb
