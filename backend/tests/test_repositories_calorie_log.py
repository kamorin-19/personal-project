from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from app.repositories.calorie_log import CalorieLogRepository


@pytest.fixture
def mock_table() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_dynamodb(mock_table: AsyncMock) -> AsyncMock:
    db = AsyncMock()
    db.Table.return_value = mock_table
    return db


@pytest.fixture
def repo(mock_dynamodb: AsyncMock) -> CalorieLogRepository:
    return CalorieLogRepository(mock_dynamodb)


class TestUpsert:
    async def test_upsert_calories(self, repo: CalorieLogRepository, mock_table: AsyncMock):
        expected = {
            "userId": "user-001",
            "recordDate": "2026-04-25",
            "calories": Decimal("2000"),
            "createdAt": "t",
            "updatedAt": "t",
        }
        mock_table.update_item.return_value = {"Attributes": expected}

        result = await repo.upsert("user-001", "2026-04-25", 2000)

        assert result == expected
        call_kwargs = mock_table.update_item.call_args.kwargs
        assert call_kwargs["Key"] == {"userId": "user-001", "recordDate": "2026-04-25"}
        assert "calories = :c" in call_kwargs["UpdateExpression"]
        assert call_kwargs["ExpressionAttributeValues"][":c"] == Decimal("2000")
        assert "if_not_exists(createdAt" in call_kwargs["UpdateExpression"]

    async def test_upsert_uses_correct_table(
        self, repo: CalorieLogRepository, mock_dynamodb: AsyncMock
    ):
        mock_dynamodb.Table.return_value.update_item.return_value = {
            "Attributes": {
                "userId": "u", "recordDate": "2026-04-25",
                "calories": Decimal("1000"), "createdAt": "t", "updatedAt": "t",
            }
        }
        await repo.upsert("u", "2026-04-25", 1000)
        mock_dynamodb.Table.assert_called_once_with("calorie_logs")


class TestListByUser:
    async def test_list_all_no_filter(self, repo: CalorieLogRepository, mock_table: AsyncMock):
        items = [{"userId": "user-001", "recordDate": "2026-04-25", "calories": Decimal("2000"), "createdAt": "t", "updatedAt": "t"}]
        mock_table.query.return_value = {"Items": items}

        result = await repo.list_by_user("user-001")

        assert result == items
        assert mock_table.query.call_args.kwargs["ScanIndexForward"] is False

    async def test_list_with_from_date(self, repo: CalorieLogRepository, mock_table: AsyncMock):
        mock_table.query.return_value = {"Items": []}
        await repo.list_by_user("user-001", from_date="2026-04-01")
        assert "KeyConditionExpression" in mock_table.query.call_args.kwargs

    async def test_list_with_to_date(self, repo: CalorieLogRepository, mock_table: AsyncMock):
        mock_table.query.return_value = {"Items": []}
        await repo.list_by_user("user-001", to_date="2026-04-30")
        assert "KeyConditionExpression" in mock_table.query.call_args.kwargs

    async def test_list_with_both_dates(self, repo: CalorieLogRepository, mock_table: AsyncMock):
        mock_table.query.return_value = {"Items": []}
        await repo.list_by_user("user-001", from_date="2026-04-01", to_date="2026-04-30")
        mock_table.query.assert_called_once()

    async def test_list_returns_empty_when_no_items(
        self, repo: CalorieLogRepository, mock_table: AsyncMock
    ):
        mock_table.query.return_value = {}
        assert await repo.list_by_user("user-001") == []


class TestDelete:
    async def test_delete_existing(self, repo: CalorieLogRepository, mock_table: AsyncMock):
        mock_table.delete_item.return_value = {"Attributes": {"userId": "user-001", "recordDate": "2026-04-25"}}
        assert await repo.delete("user-001", "2026-04-25") is True
        mock_table.delete_item.assert_called_once_with(
            Key={"userId": "user-001", "recordDate": "2026-04-25"},
            ReturnValues="ALL_OLD",
        )

    async def test_delete_nonexistent(self, repo: CalorieLogRepository, mock_table: AsyncMock):
        mock_table.delete_item.return_value = {}
        assert await repo.delete("user-001", "2026-04-25") is False
