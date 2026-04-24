from decimal import Decimal
from unittest.mock import AsyncMock, call

import pytest

from app.repositories.weight import WeightRepository


@pytest.fixture
def mock_table() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_dynamodb(mock_table: AsyncMock) -> AsyncMock:
    db = AsyncMock()
    db.Table.return_value = mock_table
    return db


@pytest.fixture
def repo(mock_dynamodb: AsyncMock) -> WeightRepository:
    return WeightRepository(mock_dynamodb)


class TestUpsert:
    async def test_upsert_with_body_fat(self, repo: WeightRepository, mock_table: AsyncMock):
        expected_item = {
            "userId": "user-001",
            "recordDate": "2026-04-25",
            "weightKg": Decimal("70.5"),
            "bodyFatPct": Decimal("15.5"),
            "createdAt": "2026-04-25T00:00:00+00:00",
            "updatedAt": "2026-04-25T00:00:00+00:00",
        }
        mock_table.update_item.return_value = {"Attributes": expected_item}

        result = await repo.upsert(
            user_id="user-001",
            record_date="2026-04-25",
            weight_kg=70.5,
            body_fat_pct=15.5,
        )

        assert result == expected_item
        mock_table.update_item.assert_called_once()
        call_kwargs = mock_table.update_item.call_args.kwargs
        assert call_kwargs["Key"] == {"userId": "user-001", "recordDate": "2026-04-25"}
        assert "bodyFatPct = :bfp" in call_kwargs["UpdateExpression"]
        assert "REMOVE" not in call_kwargs["UpdateExpression"]
        assert call_kwargs["ExpressionAttributeValues"][":wk"] == Decimal("70.5")
        assert call_kwargs["ExpressionAttributeValues"][":bfp"] == Decimal("15.5")

    async def test_upsert_without_body_fat_removes_field(
        self, repo: WeightRepository, mock_table: AsyncMock
    ):
        expected_item = {
            "userId": "user-001",
            "recordDate": "2026-04-25",
            "weightKg": Decimal("70.5"),
            "createdAt": "2026-04-25T00:00:00+00:00",
            "updatedAt": "2026-04-25T00:00:00+00:00",
        }
        mock_table.update_item.return_value = {"Attributes": expected_item}

        result = await repo.upsert(
            user_id="user-001",
            record_date="2026-04-25",
            weight_kg=70.5,
            body_fat_pct=None,
        )

        assert result == expected_item
        call_kwargs = mock_table.update_item.call_args.kwargs
        assert "REMOVE bodyFatPct" in call_kwargs["UpdateExpression"]
        assert ":bfp" not in call_kwargs["ExpressionAttributeValues"]

    async def test_upsert_uses_correct_table(self, repo: WeightRepository, mock_dynamodb: AsyncMock):
        mock_dynamodb.Table.return_value.update_item.return_value = {"Attributes": {
            "userId": "u", "recordDate": "2026-04-25", "weightKg": Decimal("70"),
            "createdAt": "t", "updatedAt": "t",
        }}
        await repo.upsert("u", "2026-04-25", 70.0, None)
        mock_dynamodb.Table.assert_called_once_with("weight_records")


class TestListByUser:
    async def test_list_all_no_filter(self, repo: WeightRepository, mock_table: AsyncMock):
        items = [
            {"userId": "user-001", "recordDate": "2026-04-25", "weightKg": Decimal("70.5"),
             "createdAt": "t", "updatedAt": "t"},
        ]
        mock_table.query.return_value = {"Items": items}

        result = await repo.list_by_user(user_id="user-001")

        assert result == items
        call_kwargs = mock_table.query.call_args.kwargs
        assert call_kwargs["ScanIndexForward"] is False

    async def test_list_with_from_date(self, repo: WeightRepository, mock_table: AsyncMock):
        mock_table.query.return_value = {"Items": []}

        await repo.list_by_user(user_id="user-001", from_date="2026-04-01")

        mock_table.query.assert_called_once()
        call_kwargs = mock_table.query.call_args.kwargs
        assert "KeyConditionExpression" in call_kwargs

    async def test_list_with_to_date(self, repo: WeightRepository, mock_table: AsyncMock):
        mock_table.query.return_value = {"Items": []}

        await repo.list_by_user(user_id="user-001", to_date="2026-04-30")

        mock_table.query.assert_called_once()

    async def test_list_with_both_dates(self, repo: WeightRepository, mock_table: AsyncMock):
        mock_table.query.return_value = {"Items": []}

        await repo.list_by_user(user_id="user-001", from_date="2026-04-01", to_date="2026-04-30")

        mock_table.query.assert_called_once()

    async def test_list_returns_empty_when_no_items(self, repo: WeightRepository, mock_table: AsyncMock):
        mock_table.query.return_value = {}

        result = await repo.list_by_user(user_id="user-001")

        assert result == []


class TestDelete:
    async def test_delete_existing_record(self, repo: WeightRepository, mock_table: AsyncMock):
        mock_table.delete_item.return_value = {
            "Attributes": {"userId": "user-001", "recordDate": "2026-04-25"}
        }

        result = await repo.delete(user_id="user-001", record_date="2026-04-25")

        assert result is True
        mock_table.delete_item.assert_called_once_with(
            Key={"userId": "user-001", "recordDate": "2026-04-25"},
            ReturnValues="ALL_OLD",
        )

    async def test_delete_nonexistent_record(self, repo: WeightRepository, mock_table: AsyncMock):
        mock_table.delete_item.return_value = {}

        result = await repo.delete(user_id="user-001", record_date="2026-04-25")

        assert result is False
