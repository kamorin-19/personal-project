from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

from boto3.dynamodb.conditions import Key

if TYPE_CHECKING:
    from types_aiobotocore_dynamodb import DynamoDBServiceResource

TABLE_NAME = "weight_records"


class WeightRepository:
    def __init__(self, dynamodb: "DynamoDBServiceResource") -> None:
        self._dynamodb = dynamodb

    async def upsert(
        self,
        user_id: str,
        record_date: str,
        weight_kg: float,
        body_fat_pct: float | None,
    ) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        table = await self._dynamodb.Table(TABLE_NAME)

        set_parts = [
            "weightKg = :wk",
            "updatedAt = :ua",
            "createdAt = if_not_exists(createdAt, :ca)",
        ]
        attr_values: dict = {
            ":wk": Decimal(str(weight_kg)),
            ":ua": now,
            ":ca": now,
        }

        if body_fat_pct is not None:
            set_parts.append("bodyFatPct = :bfp")
            attr_values[":bfp"] = Decimal(str(body_fat_pct))
            update_expression = "SET " + ", ".join(set_parts)
        else:
            update_expression = "SET " + ", ".join(set_parts) + " REMOVE bodyFatPct"

        response = await table.update_item(
            Key={"userId": user_id, "recordDate": record_date},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=attr_values,
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
