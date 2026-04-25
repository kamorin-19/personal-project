from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

from boto3.dynamodb.conditions import Key

if TYPE_CHECKING:
    from types_aiobotocore_dynamodb import DynamoDBServiceResource

TABLE_NAME = "calorie_logs"


class CalorieLogRepository:
    def __init__(self, dynamodb: "DynamoDBServiceResource") -> None:
        self._dynamodb = dynamodb

    async def upsert(self, user_id: str, record_date: str, calories: int) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        table = await self._dynamodb.Table(TABLE_NAME)

        response = await table.update_item(
            Key={"userId": user_id, "recordDate": record_date},
            UpdateExpression="SET calories = :c, updatedAt = :ua, createdAt = if_not_exists(createdAt, :ca)",
            ExpressionAttributeValues={
                ":c": Decimal(str(calories)),
                ":ua": now,
                ":ca": now,
            },
            ReturnValues="ALL_NEW",
        )
        return response["Attributes"]

    async def list_by_user(
        self,
        user_id: str,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> list[dict]:
        table = await self._dynamodb.Table(TABLE_NAME)

        key_condition = Key("userId").eq(user_id)
        if from_date and to_date:
            key_condition = key_condition & Key("recordDate").between(from_date, to_date)
        elif from_date:
            key_condition = key_condition & Key("recordDate").gte(from_date)
        elif to_date:
            key_condition = key_condition & Key("recordDate").lte(to_date)

        response = await table.query(
            KeyConditionExpression=key_condition,
            ScanIndexForward=False,
        )
        return response.get("Items", [])

    async def delete(self, user_id: str, record_date: str) -> bool:
        table = await self._dynamodb.Table(TABLE_NAME)
        response = await table.delete_item(
            Key={"userId": user_id, "recordDate": record_date},
            ReturnValues="ALL_OLD",
        )
        return bool(response.get("Attributes"))
