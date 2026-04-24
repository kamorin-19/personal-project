from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.weight import WeightRecordCreate, WeightRecordListResponse, WeightRecordResponse


class TestWeightRecordCreate:
    def test_valid_full(self):
        record = WeightRecordCreate(record_date="2026-04-25", weight_kg=70.5, body_fat_pct=15.5)
        assert record.record_date == "2026-04-25"
        assert record.weight_kg == 70.5
        assert record.body_fat_pct == 15.5

    def test_valid_without_body_fat(self):
        record = WeightRecordCreate(record_date="2026-04-25", weight_kg=70.5)
        assert record.body_fat_pct is None

    def test_invalid_date_format(self):
        with pytest.raises(ValidationError):
            WeightRecordCreate(record_date="20260425", weight_kg=70.5)

    def test_invalid_date_slash(self):
        with pytest.raises(ValidationError):
            WeightRecordCreate(record_date="2026/04/25", weight_kg=70.5)

    def test_weight_zero(self):
        with pytest.raises(ValidationError):
            WeightRecordCreate(record_date="2026-04-25", weight_kg=0)

    def test_weight_negative(self):
        with pytest.raises(ValidationError):
            WeightRecordCreate(record_date="2026-04-25", weight_kg=-1.0)

    def test_weight_over_limit(self):
        with pytest.raises(ValidationError):
            WeightRecordCreate(record_date="2026-04-25", weight_kg=301.0)

    def test_weight_at_limit(self):
        record = WeightRecordCreate(record_date="2026-04-25", weight_kg=300.0)
        assert record.weight_kg == 300.0

    def test_body_fat_negative(self):
        with pytest.raises(ValidationError):
            WeightRecordCreate(record_date="2026-04-25", weight_kg=70.0, body_fat_pct=-0.1)

    def test_body_fat_over_100(self):
        with pytest.raises(ValidationError):
            WeightRecordCreate(record_date="2026-04-25", weight_kg=70.0, body_fat_pct=100.1)

    def test_body_fat_zero_valid(self):
        record = WeightRecordCreate(record_date="2026-04-25", weight_kg=70.0, body_fat_pct=0.0)
        assert record.body_fat_pct == 0.0

    def test_body_fat_100_valid(self):
        record = WeightRecordCreate(record_date="2026-04-25", weight_kg=70.0, body_fat_pct=100.0)
        assert record.body_fat_pct == 100.0


class TestWeightRecordResponseFromDynamo:
    def test_full_item(self):
        item = {
            "recordDate": "2026-04-25",
            "weightKg": Decimal("70.5"),
            "bodyFatPct": Decimal("15.5"),
            "createdAt": "2026-04-25T00:00:00+00:00",
            "updatedAt": "2026-04-25T01:00:00+00:00",
        }
        response = WeightRecordResponse.from_dynamo(item)
        assert response.record_date == "2026-04-25"
        assert response.weight_kg == 70.5
        assert response.body_fat_pct == 15.5
        assert response.created_at == "2026-04-25T00:00:00+00:00"
        assert response.updated_at == "2026-04-25T01:00:00+00:00"

    def test_item_without_body_fat(self):
        item = {
            "recordDate": "2026-04-25",
            "weightKg": Decimal("68.0"),
            "createdAt": "2026-04-25T00:00:00+00:00",
            "updatedAt": "2026-04-25T00:00:00+00:00",
        }
        response = WeightRecordResponse.from_dynamo(item)
        assert response.body_fat_pct is None


class TestWeightRecordListResponse:
    def test_empty_list(self):
        response = WeightRecordListResponse(items=[])
        assert response.items == []

    def test_multiple_items(self):
        items = [
            WeightRecordResponse(
                record_date="2026-04-25",
                weight_kg=70.5,
                body_fat_pct=15.5,
                created_at="2026-04-25T00:00:00+00:00",
                updated_at="2026-04-25T00:00:00+00:00",
            ),
            WeightRecordResponse(
                record_date="2026-04-24",
                weight_kg=70.0,
                body_fat_pct=None,
                created_at="2026-04-24T00:00:00+00:00",
                updated_at="2026-04-24T00:00:00+00:00",
            ),
        ]
        response = WeightRecordListResponse(items=items)
        assert len(response.items) == 2
