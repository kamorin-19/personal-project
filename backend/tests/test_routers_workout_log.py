from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from tests.conftest import SAMPLE_WORKOUT_LOG_ITEM, SAMPLE_WORKOUT_LOG_ITEM_NO_WEIGHT


class TestCreateLog:
    async def test_success_with_weight(self, client: AsyncClient, mock_table):
        mock_table.put_item.return_value = {}

        response = await client.post(
            "/workout/log",
            json={
                "record_date": "2026-04-25",
                "exercise_id": "ex-uuid-001",
                "exercise_name": "ベンチプレス",
                "weight_kg": 80.0,
                "sets": [10, 8, 6],
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["record_date"] == "2026-04-25"
        assert data["exercise_id"] == "ex-uuid-001"
        assert data["exercise_name"] == "ベンチプレス"
        assert data["weight_kg"] == 80.0
        assert data["sets"] == [10, 8, 6]
        assert "log_id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_success_without_weight(self, client: AsyncClient, mock_table):
        mock_table.put_item.return_value = {}

        response = await client.post(
            "/workout/log",
            json={
                "record_date": "2026-04-25",
                "exercise_id": "ex-uuid-001",
                "exercise_name": "プッシュアップ",
                "sets": [15, 12, 10],
            },
        )

        assert response.status_code == 201
        assert response.json()["weight_kg"] is None

    async def test_invalid_date_format(self, client: AsyncClient):
        response = await client.post(
            "/workout/log",
            json={
                "record_date": "20260425",
                "exercise_id": "ex-uuid-001",
                "exercise_name": "ベンチプレス",
                "sets": [10],
            },
        )
        assert response.status_code == 422

    async def test_empty_sets(self, client: AsyncClient):
        response = await client.post(
            "/workout/log",
            json={
                "record_date": "2026-04-25",
                "exercise_id": "ex-uuid-001",
                "exercise_name": "ベンチプレス",
                "sets": [],
            },
        )
        assert response.status_code == 422

    async def test_too_many_sets(self, client: AsyncClient):
        response = await client.post(
            "/workout/log",
            json={
                "record_date": "2026-04-25",
                "exercise_id": "ex-uuid-001",
                "exercise_name": "ベンチプレス",
                "sets": [10] * 11,
            },
        )
        assert response.status_code == 422

    async def test_negative_reps(self, client: AsyncClient):
        response = await client.post(
            "/workout/log",
            json={
                "record_date": "2026-04-25",
                "exercise_id": "ex-uuid-001",
                "exercise_name": "ベンチプレス",
                "sets": [10, -1],
            },
        )
        assert response.status_code == 422

    async def test_no_auth_header(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post(
                "/workout/log",
                json={
                    "record_date": "2026-04-25",
                    "exercise_id": "ex-uuid-001",
                    "exercise_name": "ベンチプレス",
                    "sets": [10],
                },
            )
        assert response.status_code == 403

    async def test_invalid_jwt(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post(
                "/workout/log",
                json={
                    "record_date": "2026-04-25",
                    "exercise_id": "ex-uuid-001",
                    "exercise_name": "ベンチプレス",
                    "sets": [10],
                },
                headers={"Authorization": "Bearer not.a.valid.jwt"},
            )
        assert response.status_code == 401


class TestListLogs:
    async def test_success_returns_list(self, client: AsyncClient, mock_table):
        mock_table.query.return_value = {
            "Items": [SAMPLE_WORKOUT_LOG_ITEM, SAMPLE_WORKOUT_LOG_ITEM_NO_WEIGHT]
        }

        response = await client.get("/workout/log")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["items"][0]["exercise_name"] == "ベンチプレス"
        assert data["items"][1]["weight_kg"] is None

    async def test_success_empty(self, client: AsyncClient, mock_table):
        mock_table.query.return_value = {"Items": []}

        response = await client.get("/workout/log")

        assert response.status_code == 200
        assert response.json() == {"items": []}

    async def test_with_date_filters(self, client: AsyncClient, mock_table):
        mock_table.query.return_value = {"Items": [SAMPLE_WORKOUT_LOG_ITEM]}

        response = await client.get("/workout/log?from_date=2026-04-01&to_date=2026-04-30")

        assert response.status_code == 200

    async def test_no_auth(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/workout/log")
        assert response.status_code == 403


class TestDeleteLog:
    async def test_success(self, client: AsyncClient, mock_table):
        mock_table.delete_item.return_value = {
            "Attributes": {"userId": "user-001", "logId": "log-uuid-001"}
        }

        response = await client.delete("/workout/log/log-uuid-001")

        assert response.status_code == 204
        assert response.content == b""

    async def test_not_found(self, client: AsyncClient, mock_table):
        mock_table.delete_item.return_value = {}

        response = await client.delete("/workout/log/log-uuid-001")

        assert response.status_code == 404
        assert response.json()["detail"] == "Log not found"

    async def test_no_auth(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.delete("/workout/log/log-uuid-001")
        assert response.status_code == 403
