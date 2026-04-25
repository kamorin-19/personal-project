from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.workout_log import WorkoutLogCreate, WorkoutLogListResponse, WorkoutLogResponse


class TestWorkoutLogCreate:
    def test_valid_full(self):
        log = WorkoutLogCreate(
            record_date="2026-04-25",
            exercise_id="ex-uuid-001",
            exercise_name="ベンチプレス",
            weight_kg=80.0,
            sets=[10, 8, 6],
        )
        assert log.record_date == "2026-04-25"
        assert log.exercise_id == "ex-uuid-001"
        assert log.exercise_name == "ベンチプレス"
        assert log.weight_kg == 80.0
        assert log.sets == [10, 8, 6]

    def test_valid_without_weight(self):
        log = WorkoutLogCreate(
            record_date="2026-04-25",
            exercise_id="ex-uuid-001",
            exercise_name="プッシュアップ",
            sets=[15, 12, 10],
        )
        assert log.weight_kg is None

    def test_valid_single_set(self):
        log = WorkoutLogCreate(
            record_date="2026-04-25",
            exercise_id="ex-uuid-001",
            exercise_name="ベンチプレス",
            sets=[10],
        )
        assert log.sets == [10]

    def test_valid_max_sets(self):
        log = WorkoutLogCreate(
            record_date="2026-04-25",
            exercise_id="ex-uuid-001",
            exercise_name="ベンチプレス",
            sets=[10] * 10,
        )
        assert len(log.sets) == 10

    def test_invalid_date_format(self):
        with pytest.raises(ValidationError):
            WorkoutLogCreate(
                record_date="20260425",
                exercise_id="ex-uuid-001",
                exercise_name="ベンチプレス",
                sets=[10],
            )

    def test_invalid_date_slash(self):
        with pytest.raises(ValidationError):
            WorkoutLogCreate(
                record_date="2026/04/25",
                exercise_id="ex-uuid-001",
                exercise_name="ベンチプレス",
                sets=[10],
            )

    def test_empty_sets(self):
        with pytest.raises(ValidationError):
            WorkoutLogCreate(
                record_date="2026-04-25",
                exercise_id="ex-uuid-001",
                exercise_name="ベンチプレス",
                sets=[],
            )

    def test_too_many_sets(self):
        with pytest.raises(ValidationError):
            WorkoutLogCreate(
                record_date="2026-04-25",
                exercise_id="ex-uuid-001",
                exercise_name="ベンチプレス",
                sets=[10] * 11,
            )

    def test_negative_reps(self):
        with pytest.raises(ValidationError):
            WorkoutLogCreate(
                record_date="2026-04-25",
                exercise_id="ex-uuid-001",
                exercise_name="ベンチプレス",
                sets=[10, -1, 8],
            )

    def test_weight_negative(self):
        with pytest.raises(ValidationError):
            WorkoutLogCreate(
                record_date="2026-04-25",
                exercise_id="ex-uuid-001",
                exercise_name="ベンチプレス",
                weight_kg=-1.0,
                sets=[10],
            )

    def test_weight_over_limit(self):
        with pytest.raises(ValidationError):
            WorkoutLogCreate(
                record_date="2026-04-25",
                exercise_id="ex-uuid-001",
                exercise_name="ベンチプレス",
                weight_kg=1000.0,
                sets=[10],
            )

    def test_weight_zero_valid(self):
        log = WorkoutLogCreate(
            record_date="2026-04-25",
            exercise_id="ex-uuid-001",
            exercise_name="ベンチプレス",
            weight_kg=0.0,
            sets=[10],
        )
        assert log.weight_kg == 0.0

    def test_weight_at_limit(self):
        log = WorkoutLogCreate(
            record_date="2026-04-25",
            exercise_id="ex-uuid-001",
            exercise_name="ベンチプレス",
            weight_kg=999.0,
            sets=[10],
        )
        assert log.weight_kg == 999.0

    def test_empty_exercise_id(self):
        with pytest.raises(ValidationError):
            WorkoutLogCreate(
                record_date="2026-04-25",
                exercise_id="",
                exercise_name="ベンチプレス",
                sets=[10],
            )

    def test_empty_exercise_name(self):
        with pytest.raises(ValidationError):
            WorkoutLogCreate(
                record_date="2026-04-25",
                exercise_id="ex-uuid-001",
                exercise_name="",
                sets=[10],
            )

    def test_exercise_name_too_long(self):
        with pytest.raises(ValidationError):
            WorkoutLogCreate(
                record_date="2026-04-25",
                exercise_id="ex-uuid-001",
                exercise_name="a" * 101,
                sets=[10],
            )


class TestWorkoutLogResponseFromDynamo:
    def test_full_item(self):
        item = {
            "logId": "log-uuid-001",
            "recordDate": "2026-04-25",
            "exerciseId": "ex-uuid-001",
            "exerciseName": "ベンチプレス",
            "weightKg": Decimal("80.0"),
            "sets": [10, 8, 6],
            "createdAt": "2026-04-25T00:00:00+00:00",
            "updatedAt": "2026-04-25T01:00:00+00:00",
        }
        response = WorkoutLogResponse.from_dynamo(item)
        assert response.log_id == "log-uuid-001"
        assert response.record_date == "2026-04-25"
        assert response.exercise_id == "ex-uuid-001"
        assert response.exercise_name == "ベンチプレス"
        assert response.weight_kg == 80.0
        assert response.sets == [10, 8, 6]
        assert response.created_at == "2026-04-25T00:00:00+00:00"
        assert response.updated_at == "2026-04-25T01:00:00+00:00"

    def test_item_without_weight(self):
        item = {
            "logId": "log-uuid-001",
            "recordDate": "2026-04-25",
            "exerciseId": "ex-uuid-001",
            "exerciseName": "プッシュアップ",
            "sets": [15, 12],
            "createdAt": "2026-04-25T00:00:00+00:00",
            "updatedAt": "2026-04-25T00:00:00+00:00",
        }
        response = WorkoutLogResponse.from_dynamo(item)
        assert response.weight_kg is None

    def test_sets_with_decimal_values(self):
        item = {
            "logId": "log-uuid-001",
            "recordDate": "2026-04-25",
            "exerciseId": "ex-uuid-001",
            "exerciseName": "ベンチプレス",
            "sets": [Decimal("10"), Decimal("8"), Decimal("6")],
            "createdAt": "t",
            "updatedAt": "t",
        }
        response = WorkoutLogResponse.from_dynamo(item)
        assert response.sets == [10, 8, 6]
        assert all(isinstance(s, int) for s in response.sets)


class TestWorkoutLogListResponse:
    def test_empty_list(self):
        response = WorkoutLogListResponse(items=[])
        assert response.items == []

    def test_multiple_items(self):
        items = [
            WorkoutLogResponse(
                log_id="log-001",
                record_date="2026-04-25",
                exercise_id="ex-001",
                exercise_name="ベンチプレス",
                weight_kg=80.0,
                sets=[10, 8],
                created_at="2026-04-25T00:00:00+00:00",
                updated_at="2026-04-25T00:00:00+00:00",
            ),
            WorkoutLogResponse(
                log_id="log-002",
                record_date="2026-04-25",
                exercise_id="ex-002",
                exercise_name="スクワット",
                weight_kg=None,
                sets=[15, 12, 10],
                created_at="2026-04-25T00:00:00+00:00",
                updated_at="2026-04-25T00:00:00+00:00",
            ),
        ]
        response = WorkoutLogListResponse(items=items)
        assert len(response.items) == 2
        assert response.items[0].exercise_name == "ベンチプレス"
        assert response.items[1].weight_kg is None
