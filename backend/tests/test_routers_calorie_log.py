from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from tests.conftest import SAMPLE_CALORIE_LOG_ITEM


class TestUpsertCalorie:
    async def test_success(self, client: AsyncClient, mock_table):
        mock_table.update_item.return_value = {"Attributes": SAMPLE_CALORIE_LOG_ITEM}

        response = await client.post(
            "/workout/calorie",
            json={"record_date": "2026-04-25", "calories": 2000},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["record_date"] == "2026-04-25"
        assert data["calories"] == 2000
        assert "created_at" in data
        assert "updated_at" in data

    async def test_calories_zero(self, client: AsyncClient, mock_table):
        mock_table.update_item.return_value = {
            "Attributes": {**SAMPLE_CALORIE_LOG_ITEM, "calories": Decimal("0")}
        }
        response = await client.post(
            "/workout/calorie",
            json={"record_date": "2026-04-25", "calories": 0},
        )
        assert response.status_code == 200
        assert response.json()["calories"] == 0

    async def test_invalid_date_format(self, client: AsyncClient):
        response = await client.post(
            "/workout/calorie",
            json={"record_date": "20260425", "calories": 2000},
        )
        assert response.status_code == 422

    async def test_calories_negative(self, client: AsyncClient):
        response = await client.post(
            "/workout/calorie",
            json={"record_date": "2026-04-25", "calories": -1},
        )
        assert response.status_code == 422

    async def test_calories_over_limit(self, client: AsyncClient):
        response = await client.post(
            "/workout/calorie",
            json={"record_date": "2026-04-25", "calories": 100000},
        )
        assert response.status_code == 422

    async def test_no_auth(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post(
                "/workout/calorie",
                json={"record_date": "2026-04-25", "calories": 2000},
            )
        assert response.status_code == 403

    async def test_invalid_jwt(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post(
                "/workout/calorie",
                json={"record_date": "2026-04-25", "calories": 2000},
                headers={"Authorization": "Bearer not.a.valid.jwt"},
            )
        assert response.status_code == 401


class TestListCalorie:
    async def test_success(self, client: AsyncClient, mock_table):
        mock_table.query.return_value = {"Items": [SAMPLE_CALORIE_LOG_ITEM]}

        response = await client.get("/workout/calorie")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["calories"] == 2000

    async def test_empty(self, client: AsyncClient, mock_table):
        mock_table.query.return_value = {"Items": []}
        response = await client.get("/workout/calorie")
        assert response.status_code == 200
        assert response.json() == {"items": []}

    async def test_with_date_filters(self, client: AsyncClient, mock_table):
        mock_table.query.return_value = {"Items": [SAMPLE_CALORIE_LOG_ITEM]}
        response = await client.get("/workout/calorie?from_date=2026-04-01&to_date=2026-04-30")
        assert response.status_code == 200

    async def test_no_auth(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/workout/calorie")
        assert response.status_code == 403


class TestDeleteCalorie:
    async def test_success(self, client: AsyncClient, mock_table):
        mock_table.delete_item.return_value = {
            "Attributes": {"userId": "user-001", "recordDate": "2026-04-25"}
        }
        response = await client.delete("/workout/calorie/2026-04-25")
        assert response.status_code == 204
        assert response.content == b""

    async def test_not_found(self, client: AsyncClient, mock_table):
        mock_table.delete_item.return_value = {}
        response = await client.delete("/workout/calorie/2026-04-25")
        assert response.status_code == 404
        assert response.json()["detail"] == "Record not found"

    async def test_no_auth(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.delete("/workout/calorie/2026-04-25")
        assert response.status_code == 403
