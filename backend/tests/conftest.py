from decimal import Decimal
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.dependencies import get_current_user, get_dynamodb
from app.main import app

TEST_USER = {"user_id": "user-001", "email": "test@example.com", "name": "Test User"}

SAMPLE_DYNAMO_ITEM = {
    "userId": "user-001",
    "recordDate": "2026-04-25",
    "weightKg": Decimal("70.5"),
    "bodyFatPct": Decimal("15.5"),
    "createdAt": "2026-04-25T00:00:00+00:00",
    "updatedAt": "2026-04-25T00:00:00+00:00",
}

SAMPLE_DYNAMO_ITEM_NO_FAT = {
    "userId": "user-001",
    "recordDate": "2026-04-24",
    "weightKg": Decimal("69.0"),
    "createdAt": "2026-04-24T00:00:00+00:00",
    "updatedAt": "2026-04-24T00:00:00+00:00",
}

SAMPLE_EXERCISE_ITEM = {
    "userId": "user-001",
    "exerciseId": "ex-uuid-001",
    "name": "ベンチプレス",
    "muscleGroup": "chest",
    "caloriesPerRepPerKg": Decimal("0.050"),
    "createdAt": "2026-04-25T00:00:00+00:00",
    "updatedAt": "2026-04-25T00:00:00+00:00",
}

SAMPLE_EXERCISE_ITEM_NO_CALORIES = {
    "userId": "user-001",
    "exerciseId": "ex-uuid-002",
    "name": "スクワット",
    "muscleGroup": "leg",
    "createdAt": "2026-04-25T00:00:00+00:00",
    "updatedAt": "2026-04-25T00:00:00+00:00",
}


@pytest.fixture
def mock_table() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_dynamodb(mock_table: AsyncMock) -> AsyncMock:
    db = AsyncMock()
    db.Table.return_value = mock_table
    return db


@pytest_asyncio.fixture
async def client(mock_dynamodb: AsyncMock) -> AsyncClient:
    async def override_get_dynamodb():
        yield mock_dynamodb

    app.dependency_overrides[get_dynamodb] = override_get_dynamodb
    app.dependency_overrides[get_current_user] = lambda: TEST_USER

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
