from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.calorie_log import CalorieLogCreate, CalorieLogListResponse, CalorieLogResponse


class TestCalorieLogCreate:
    def test_valid(self):
        log = CalorieLogCreate(record_date="2026-04-25", calories=2000)
        assert log.record_date == "2026-04-25"
        assert log.calories == 2000

    def test_calories_zero_valid(self):
        log = CalorieLogCreate(record_date="2026-04-25", calories=0)
        assert log.calories == 0

    def test_calories_at_limit(self):
        log = CalorieLogCreate(record_date="2026-04-25", calories=99999)
        assert log.calories == 99999

    def test_calories_negative(self):
        with pytest.raises(ValidationError):
            CalorieLogCreate(record_date="2026-04-25", calories=-1)

    def test_calories_over_limit(self):
        with pytest.raises(ValidationError):
            CalorieLogCreate(record_date="2026-04-25", calories=100000)

    def test_invalid_date_format(self):
        with pytest.raises(ValidationError):
            CalorieLogCreate(record_date="20260425", calories=2000)

    def test_invalid_date_slash(self):
        with pytest.raises(ValidationError):
            CalorieLogCreate(record_date="2026/04/25", calories=2000)


class TestCalorieLogResponseFromDynamo:
    def test_full_item(self):
        item = {
            "recordDate": "2026-04-25",
            "calories": Decimal("2000"),
            "createdAt": "2026-04-25T00:00:00+00:00",
            "updatedAt": "2026-04-25T01:00:00+00:00",
        }
        response = CalorieLogResponse.from_dynamo(item)
        assert response.record_date == "2026-04-25"
        assert response.calories == 2000
        assert isinstance(response.calories, int)
        assert response.created_at == "2026-04-25T00:00:00+00:00"
        assert response.updated_at == "2026-04-25T01:00:00+00:00"


class TestCalorieLogListResponse:
    def test_empty_list(self):
        assert CalorieLogListResponse(items=[]).items == []

    def test_multiple_items(self):
        items = [
            CalorieLogResponse(
                record_date="2026-04-25",
                calories=2000,
                created_at="t",
                updated_at="t",
            ),
            CalorieLogResponse(
                record_date="2026-04-24",
                calories=1800,
                created_at="t",
                updated_at="t",
            ),
        ]
        response = CalorieLogListResponse(items=items)
        assert len(response.items) == 2
