from decimal import Decimal
from unittest.mock import ANY, AsyncMock

import pytest

from app.repositories.exercise import ExerciseRepository


@pytest.fixture
def mock_table() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_dynamodb(mock_table: AsyncMock) -> AsyncMock:
    db = AsyncMock()
    db.Table.return_value = mock_table
    return db


@pytest.fixture
def repo(mock_dynamodb: AsyncMock) -> ExerciseRepository:
    return ExerciseRepository(mock_dynamodb)


class TestCreate:
    async def test_create_with_calories(self, repo: ExerciseRepository, mock_table: AsyncMock):
        mock_table.put_item.return_value = {}

        result = await repo.create(
            user_id="user-001",
            name="ベンチプレス",
            muscle_group="chest",
            calories_per_rep_per_kg=0.05,
        )

        assert result["userId"] == "user-001"
        assert result["name"] == "ベンチプレス"
        assert result["muscleGroup"] == "chest"
        assert result["caloriesPerRepPerKg"] == Decimal("0.05")
        assert "exerciseId" in result
        assert "createdAt" in result
        assert "updatedAt" in result

    async def test_create_without_calories(self, repo: ExerciseRepository, mock_table: AsyncMock):
        mock_table.put_item.return_value = {}

        result = await repo.create(
            user_id="user-001",
            name="スクワット",
            muscle_group="leg",
            calories_per_rep_per_kg=None,
        )

        assert "caloriesPerRepPerKg" not in result

    async def test_create_generates_unique_exercise_id(
        self, repo: ExerciseRepository, mock_table: AsyncMock
    ):
        mock_table.put_item.return_value = {}

        result1 = await repo.create("user-001", "種目A", "chest", None)
        result2 = await repo.create("user-001", "種目B", "back", None)

        assert result1["exerciseId"] != result2["exerciseId"]

    async def test_create_calls_put_item(self, repo: ExerciseRepository, mock_table: AsyncMock):
        mock_table.put_item.return_value = {}

        await repo.create("user-001", "ベンチプレス", "chest", 0.05)

        mock_table.put_item.assert_called_once_with(Item=ANY)

    async def test_create_uses_correct_table(
        self, repo: ExerciseRepository, mock_dynamodb: AsyncMock
    ):
        mock_dynamodb.Table.return_value.put_item.return_value = {}

        await repo.create("user-001", "ベンチプレス", "chest", None)

        mock_dynamodb.Table.assert_called_once_with("exercises")


class TestListByUser:
    async def test_list_returns_items(self, repo: ExerciseRepository, mock_table: AsyncMock):
        items = [
            {
                "userId": "user-001",
                "exerciseId": "ex-001",
                "name": "ベンチプレス",
                "muscleGroup": "chest",
                "createdAt": "t",
                "updatedAt": "t",
            },
        ]
        mock_table.query.return_value = {"Items": items}

        result = await repo.list_by_user(user_id="user-001")

        assert result == items
        mock_table.query.assert_called_once()

    async def test_list_returns_empty_when_no_items(
        self, repo: ExerciseRepository, mock_table: AsyncMock
    ):
        mock_table.query.return_value = {"Items": []}

        result = await repo.list_by_user(user_id="user-001")

        assert result == []

    async def test_list_returns_empty_when_key_missing(
        self, repo: ExerciseRepository, mock_table: AsyncMock
    ):
        mock_table.query.return_value = {}

        result = await repo.list_by_user(user_id="user-001")

        assert result == []


class TestDelete:
    async def test_delete_existing_exercise(
        self, repo: ExerciseRepository, mock_table: AsyncMock
    ):
        mock_table.delete_item.return_value = {
            "Attributes": {"userId": "user-001", "exerciseId": "ex-uuid-001"}
        }

        result = await repo.delete(user_id="user-001", exercise_id="ex-uuid-001")

        assert result is True
        mock_table.delete_item.assert_called_once_with(
            Key={"userId": "user-001", "exerciseId": "ex-uuid-001"},
            ReturnValues="ALL_OLD",
        )

    async def test_delete_nonexistent_exercise(
        self, repo: ExerciseRepository, mock_table: AsyncMock
    ):
        mock_table.delete_item.return_value = {}

        result = await repo.delete(user_id="user-001", exercise_id="ex-uuid-001")

        assert result is False
