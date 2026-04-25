from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from app.repositories.workout_log import WorkoutLogRepository


@pytest.fixture
def mock_table() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_dynamodb(mock_table: AsyncMock) -> AsyncMock:
    db = AsyncMock()
    db.Table.return_value = mock_table
    return db


@pytest.fixture
def repo(mock_dynamodb: AsyncMock) -> WorkoutLogRepository:
    return WorkoutLogRepository(mock_dynamodb)


class TestCreate:
    async def test_create_with_weight(self, repo: WorkoutLogRepository, mock_table: AsyncMock):
        mock_table.put_item.return_value = {}

        result = await repo.create(
            user_id="user-001",
            record_date="2026-04-25",
            exercise_id="ex-uuid-001",
            exercise_name="ベンチプレス",
            weight_kg=80.0,
            sets=[10, 8, 6],
        )

        assert result["userId"] == "user-001"
        assert result["recordDate"] == "2026-04-25"
        assert result["exerciseId"] == "ex-uuid-001"
        assert result["exerciseName"] == "ベンチプレス"
        assert result["weightKg"] == Decimal("80.0")
        assert result["sets"] == [10, 8, 6]
        assert "logId" in result
        assert "createdAt" in result
        assert "updatedAt" in result
        mock_table.put_item.assert_called_once()

    async def test_create_without_weight(self, repo: WorkoutLogRepository, mock_table: AsyncMock):
        mock_table.put_item.return_value = {}

        result = await repo.create(
            user_id="user-001",
            record_date="2026-04-25",
            exercise_id="ex-uuid-001",
            exercise_name="プッシュアップ",
            weight_kg=None,
            sets=[15, 12, 10],
        )

        assert "weightKg" not in result
        mock_table.put_item.assert_called_once()

    async def test_create_generates_unique_log_id(
        self, repo: WorkoutLogRepository, mock_table: AsyncMock
    ):
        mock_table.put_item.return_value = {}

        result1 = await repo.create("u", "2026-04-25", "ex-001", "ベンチプレス", 80.0, [10])
        result2 = await repo.create("u", "2026-04-25", "ex-001", "ベンチプレス", 80.0, [10])

        assert result1["logId"] != result2["logId"]

    async def test_create_uses_correct_table(
        self, repo: WorkoutLogRepository, mock_dynamodb: AsyncMock
    ):
        mock_dynamodb.Table.return_value.put_item.return_value = {}

        await repo.create("u", "2026-04-25", "ex-001", "ベンチプレス", 80.0, [10])

        mock_dynamodb.Table.assert_called_once_with("workout_logs")

    async def test_create_item_passed_to_put(
        self, repo: WorkoutLogRepository, mock_table: AsyncMock
    ):
        mock_table.put_item.return_value = {}

        await repo.create("user-001", "2026-04-25", "ex-001", "ベンチプレス", 100.0, [5, 5])

        call_kwargs = mock_table.put_item.call_args.kwargs
        assert "Item" in call_kwargs
        item = call_kwargs["Item"]
        assert item["userId"] == "user-001"
        assert item["recordDate"] == "2026-04-25"


class TestListByUser:
    async def test_list_all_no_filter(self, repo: WorkoutLogRepository, mock_table: AsyncMock):
        items = [
            {
                "userId": "user-001",
                "logId": "log-001",
                "recordDate": "2026-04-25",
                "exerciseId": "ex-001",
                "exerciseName": "ベンチプレス",
                "weightKg": Decimal("80.0"),
                "sets": [10, 8, 6],
                "createdAt": "t",
                "updatedAt": "t",
            }
        ]
        mock_table.query.return_value = {"Items": items}

        result = await repo.list_by_user(user_id="user-001")

        assert result == items
        call_kwargs = mock_table.query.call_args.kwargs
        assert call_kwargs["ScanIndexForward"] is False
        assert "FilterExpression" not in call_kwargs

    async def test_list_with_from_date(self, repo: WorkoutLogRepository, mock_table: AsyncMock):
        mock_table.query.return_value = {"Items": []}

        await repo.list_by_user(user_id="user-001", from_date="2026-04-01")

        call_kwargs = mock_table.query.call_args.kwargs
        assert "FilterExpression" in call_kwargs

    async def test_list_with_to_date(self, repo: WorkoutLogRepository, mock_table: AsyncMock):
        mock_table.query.return_value = {"Items": []}

        await repo.list_by_user(user_id="user-001", to_date="2026-04-30")

        call_kwargs = mock_table.query.call_args.kwargs
        assert "FilterExpression" in call_kwargs

    async def test_list_with_both_dates(self, repo: WorkoutLogRepository, mock_table: AsyncMock):
        mock_table.query.return_value = {"Items": []}

        await repo.list_by_user(
            user_id="user-001", from_date="2026-04-01", to_date="2026-04-30"
        )

        call_kwargs = mock_table.query.call_args.kwargs
        assert "FilterExpression" in call_kwargs

    async def test_list_returns_empty_when_no_items(
        self, repo: WorkoutLogRepository, mock_table: AsyncMock
    ):
        mock_table.query.return_value = {}

        result = await repo.list_by_user(user_id="user-001")

        assert result == []


class TestDelete:
    async def test_delete_existing_record(
        self, repo: WorkoutLogRepository, mock_table: AsyncMock
    ):
        mock_table.delete_item.return_value = {
            "Attributes": {"userId": "user-001", "logId": "log-001"}
        }

        result = await repo.delete(user_id="user-001", log_id="log-001")

        assert result is True
        mock_table.delete_item.assert_called_once_with(
            Key={"userId": "user-001", "logId": "log-001"},
            ReturnValues="ALL_OLD",
        )

    async def test_delete_nonexistent_record(
        self, repo: WorkoutLogRepository, mock_table: AsyncMock
    ):
        mock_table.delete_item.return_value = {}

        result = await repo.delete(user_id="user-001", log_id="log-001")

        assert result is False
