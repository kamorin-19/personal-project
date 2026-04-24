import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from tests.conftest import SAMPLE_EXERCISE_ITEM, SAMPLE_EXERCISE_ITEM_NO_CALORIES


class TestCreateExercise:
    async def test_success_with_calories(self, client: AsyncClient, mock_table):
        mock_table.put_item.return_value = {}
        mock_table.put_item.side_effect = None

        # create() returns the item directly, so patch at router level via mock_table
        # We configure the mock to make the repo.create() return a proper item
        # by overriding put_item and relying on the repo building the return value itself
        response = await client.post(
            "/workout/exercise",
            json={"name": "ベンチプレス", "muscle_group": "chest", "calories_per_rep_per_kg": 0.05},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "ベンチプレス"
        assert data["muscle_group"] == "chest"
        assert data["calories_per_rep_per_kg"] == 0.05
        assert "exercise_id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_success_without_calories(self, client: AsyncClient, mock_table):
        mock_table.put_item.return_value = {}

        response = await client.post(
            "/workout/exercise",
            json={"name": "スクワット", "muscle_group": "leg"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["calories_per_rep_per_kg"] is None

    async def test_name_empty_invalid(self, client: AsyncClient):
        response = await client.post(
            "/workout/exercise",
            json={"name": "", "muscle_group": "chest"},
        )
        assert response.status_code == 422

    async def test_invalid_muscle_group(self, client: AsyncClient):
        response = await client.post(
            "/workout/exercise",
            json={"name": "種目", "muscle_group": "invalid"},
        )
        assert response.status_code == 422

    async def test_calories_negative_invalid(self, client: AsyncClient):
        response = await client.post(
            "/workout/exercise",
            json={"name": "種目", "muscle_group": "chest", "calories_per_rep_per_kg": -0.001},
        )
        assert response.status_code == 422

    async def test_no_auth(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post(
                "/workout/exercise",
                json={"name": "ベンチプレス", "muscle_group": "chest"},
            )
        assert response.status_code == 403

    async def test_invalid_jwt(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post(
                "/workout/exercise",
                json={"name": "ベンチプレス", "muscle_group": "chest"},
                headers={"Authorization": "Bearer not.a.valid.jwt"},
            )
        assert response.status_code == 401


class TestListExercises:
    async def test_success_returns_list(self, client: AsyncClient, mock_table):
        mock_table.query.return_value = {
            "Items": [SAMPLE_EXERCISE_ITEM, SAMPLE_EXERCISE_ITEM_NO_CALORIES]
        }

        response = await client.get("/workout/exercise")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["items"][0]["name"] == "ベンチプレス"
        assert data["items"][0]["calories_per_rep_per_kg"] == 0.05
        assert data["items"][1]["calories_per_rep_per_kg"] is None

    async def test_success_empty(self, client: AsyncClient, mock_table):
        mock_table.query.return_value = {"Items": []}

        response = await client.get("/workout/exercise")

        assert response.status_code == 200
        assert response.json() == {"items": []}

    async def test_no_auth(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/workout/exercise")
        assert response.status_code == 403


class TestDeleteExercise:
    async def test_success(self, client: AsyncClient, mock_table):
        mock_table.delete_item.return_value = {
            "Attributes": {"userId": "user-001", "exerciseId": "ex-uuid-001"}
        }

        response = await client.delete("/workout/exercise/ex-uuid-001")

        assert response.status_code == 204
        assert response.content == b""

    async def test_not_found(self, client: AsyncClient, mock_table):
        mock_table.delete_item.return_value = {}

        response = await client.delete("/workout/exercise/ex-uuid-001")

        assert response.status_code == 404
        assert response.json()["detail"] == "Exercise not found"

    async def test_no_auth(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.delete("/workout/exercise/ex-uuid-001")
        assert response.status_code == 403
