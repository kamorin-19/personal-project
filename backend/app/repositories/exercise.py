import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

from boto3.dynamodb.conditions import Key

if TYPE_CHECKING:
    from types_aiobotocore_dynamodb import DynamoDBServiceResource

TABLE_NAME = "exercises"


class ExerciseRepository:
    def __init__(self, dynamodb: "DynamoDBServiceResource") -> None:
        self._dynamodb = dynamodb

    async def create(
        self,
        user_id: str,
        name: str,
        muscle_group: str,
        calories_per_rep_per_kg: float | None,
    ) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        exercise_id = str(uuid.uuid4())
        table = await self._dynamodb.Table(TABLE_NAME)

        item: dict = {
            "userId": user_id,
            "exerciseId": exercise_id,
            "name": name,
            "muscleGroup": muscle_group,
            "createdAt": now,
            "updatedAt": now,
        }
        if calories_per_rep_per_kg is not None:
            item["caloriesPerRepPerKg"] = Decimal(str(calories_per_rep_per_kg))

        await table.put_item(Item=item)
        return item

    async def list_by_user(self, user_id: str) -> list[dict]:
        table = await self._dynamodb.Table(TABLE_NAME)
        response = await table.query(
            KeyConditionExpression=Key("userId").eq(user_id),
        )
        return response.get("Items", [])

    async def delete(self, user_id: str, exercise_id: str) -> bool:
        table = await self._dynamodb.Table(TABLE_NAME)
        response = await table.delete_item(
            Key={"userId": user_id, "exerciseId": exercise_id},
            ReturnValues="ALL_OLD",
        )
        return bool(response.get("Attributes"))
