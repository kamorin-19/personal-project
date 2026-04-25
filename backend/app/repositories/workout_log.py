import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

from boto3.dynamodb.conditions import Attr, Key

if TYPE_CHECKING:
    from types_aiobotocore_dynamodb import DynamoDBServiceResource

TABLE_NAME = "workout_logs"


class WorkoutLogRepository:
    def __init__(self, dynamodb: "DynamoDBServiceResource") -> None:
        self._dynamodb = dynamodb

    async def create(
        self,
        user_id: str,
        record_date: str,
        exercise_id: str,
        exercise_name: str,
        weight_kg: float | None,
        sets: list[int],
    ) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        log_id = str(uuid.uuid4())
        table = await self._dynamodb.Table(TABLE_NAME)

        item: dict = {
            "userId": user_id,
            "logId": log_id,
            "recordDate": record_date,
            "exerciseId": exercise_id,
            "exerciseName": exercise_name,
            "sets": [int(s) for s in sets],
            "createdAt": now,
            "updatedAt": now,
        }
        if weight_kg is not None:
            item["weightKg"] = Decimal(str(weight_kg))

        await table.put_item(Item=item)
        return item

    async def list_by_user(
        self,
        user_id: str,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> list[dict]:
        table = await self._dynamodb.Table(TABLE_NAME)

        kwargs: dict = {
            "KeyConditionExpression": Key("userId").eq(user_id),
            "ScanIndexForward": False,
        }

        if from_date and to_date:
            kwargs["FilterExpression"] = Attr("recordDate").between(from_date, to_date)
        elif from_date:
            kwargs["FilterExpression"] = Attr("recordDate").gte(from_date)
        elif to_date:
            kwargs["FilterExpression"] = Attr("recordDate").lte(to_date)

        response = await table.query(**kwargs)
        return response.get("Items", [])

    async def delete(self, user_id: str, log_id: str) -> bool:
        table = await self._dynamodb.Table(TABLE_NAME)
        response = await table.delete_item(
            Key={"userId": user_id, "logId": log_id},
            ReturnValues="ALL_OLD",
        )
        return bool(response.get("Attributes"))
