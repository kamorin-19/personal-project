from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from tests.conftest import SAMPLE_DYNAMO_ITEM, SAMPLE_DYNAMO_ITEM_NO_FAT


class TestUpsertWeight:
    async def test_success_with_body_fat(self, client: AsyncClient, mock_table):
        mock_table.update_item.return_value = {"Attributes": SAMPLE_DYNAMO_ITEM}

        response = await client.post(
            "/workout/weight",
            json={"record_date": "2026-04-25", "weight_kg": 70.5, "body_fat_pct": 15.5},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["record_date"] == "2026-04-25"
        assert data["weight_kg"] == 70.5
        assert data["body_fat_pct"] == 15.5
        assert "created_at" in data
        assert "updated_at" in data

    async def test_success_without_body_fat(self, client: AsyncClient, mock_table):
        mock_table.update_item.return_value = {"Attributes": SAMPLE_DYNAMO_ITEM_NO_FAT}

        response = await client.post(
            "/workout/weight",
            json={"record_date": "2026-04-24", "weight_kg": 69.0},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["body_fat_pct"] is None

    async def test_invalid_date_format(self, client: AsyncClient):
        response = await client.post(
            "/workout/weight",
            json={"record_date": "20260425", "weight_kg": 70.5},
        )
        assert response.status_code == 422

    async def test_weight_zero(self, client: AsyncClient):
        response = await client.post(
            "/workout/weight",
            json={"record_date": "2026-04-25", "weight_kg": 0},
        )
        assert response.status_code == 422

    async def test_weight_over_limit(self, client: AsyncClient):
        response = await client.post(
            "/workout/weight",
            json={"record_date": "2026-04-25", "weight_kg": 301.0},
        )
        assert response.status_code == 422

    async def test_no_auth_header(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post(
                "/workout/weight",
                json={"record_date": "2026-04-25", "weight_kg": 70.5},
            )
        assert response.status_code == 403

    async def test_invalid_jwt(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post(
                "/workout/weight",
                json={"record_date": "2026-04-25", "weight_kg": 70.5},
                headers={"Authorization": "Bearer not.a.valid.jwt"},
            )
        assert response.status_code == 401


class TestListWeight:
    async def test_success_returns_list(self, client: AsyncClient, mock_table):
        mock_table.query.return_value = {"Items": [SAMPLE_DYNAMO_ITEM, SAMPLE_DYNAMO_ITEM_NO_FAT]}

        response = await client.get("/workout/weight")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["items"][0]["record_date"] == "2026-04-25"
        assert data["items"][1]["body_fat_pct"] is None

    async def test_success_empty(self, client: AsyncClient, mock_table):
        mock_table.query.return_value = {"Items": []}

        response = await client.get("/workout/weight")

        assert response.status_code == 200
        assert response.json() == {"items": []}

    async def test_with_date_filters(self, client: AsyncClient, mock_table):
        mock_table.query.return_value = {"Items": [SAMPLE_DYNAMO_ITEM]}

        response = await client.get("/workout/weight?from_date=2026-04-01&to_date=2026-04-30")

        assert response.status_code == 200

    async def test_no_auth(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/workout/weight")
        assert response.status_code == 403


class TestDeleteWeight:
    async def test_success(self, client: AsyncClient, mock_table):
        mock_table.delete_item.return_value = {
            "Attributes": {"userId": "user-001", "recordDate": "2026-04-25"}
        }

        response = await client.delete("/workout/weight/2026-04-25")

        assert response.status_code == 204
        assert response.content == b""

    async def test_not_found(self, client: AsyncClient, mock_table):
        mock_table.delete_item.return_value = {}

        response = await client.delete("/workout/weight/2026-04-25")

        assert response.status_code == 404
        assert response.json()["detail"] == "Record not found"

    async def test_no_auth(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.delete("/workout/weight/2026-04-25")
        assert response.status_code == 403
