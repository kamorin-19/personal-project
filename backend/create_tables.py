"""DynamoDB テーブル作成スクリプト。

ローカル開発 (DynamoDB Local) および本番 AWS 両対応。
DYNAMODB_ENDPOINT_URL が設定されていればローカル、未設定なら本番 AWS に接続する。

Usage:
    cd backend && python create_tables.py
"""

import asyncio

import aioboto3
from botocore.exceptions import ClientError

from app.config import settings

TABLES = [
    {
        "TableName": "weight_records",
        "KeySchema": [
            {"AttributeName": "userId", "KeyType": "HASH"},
            {"AttributeName": "recordDate", "KeyType": "RANGE"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "userId", "AttributeType": "S"},
            {"AttributeName": "recordDate", "AttributeType": "S"},
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },
]


async def create_table(client, table_def: dict) -> None:
    name = table_def["TableName"]
    try:
        await client.create_table(**table_def)
        print(f"Created : {name}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"Exists  : {name}")
        else:
            raise


async def main() -> None:
    kwargs: dict = {
        "region_name": settings.aws_region,
        "aws_access_key_id": settings.aws_access_key_id,
        "aws_secret_access_key": settings.aws_secret_access_key,
    }
    if settings.dynamodb_endpoint_url:
        kwargs["endpoint_url"] = settings.dynamodb_endpoint_url
        print(f"Target  : {settings.dynamodb_endpoint_url} (local)")
    else:
        print(f"Target  : AWS DynamoDB ({settings.aws_region})")

    async with aioboto3.Session().client("dynamodb", **kwargs) as client:
        for table_def in TABLES:
            await create_table(client, table_def)

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
