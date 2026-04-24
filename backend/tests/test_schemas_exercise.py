from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.exercise import (
    ExerciseCreate,
    ExerciseListResponse,
    ExerciseResponse,
    MuscleGroup,
)


class TestExerciseCreate:
    def test_valid_full(self):
        record = ExerciseCreate(
            name="ベンチプレス",
            muscle_group=MuscleGroup.chest,
            calories_per_rep_per_kg=0.05,
        )
        assert record.name == "ベンチプレス"
        assert record.muscle_group == MuscleGroup.chest
        assert record.calories_per_rep_per_kg == 0.05

    def test_valid_without_calories(self):
        record = ExerciseCreate(name="スクワット", muscle_group=MuscleGroup.leg)
        assert record.calories_per_rep_per_kg is None

    def test_all_muscle_groups_accepted(self):
        for group in MuscleGroup:
            record = ExerciseCreate(name="種目", muscle_group=group)
            assert record.muscle_group == group

    def test_muscle_group_string_value(self):
        record = ExerciseCreate(name="種目", muscle_group="back")
        assert record.muscle_group == MuscleGroup.back

    def test_name_empty_string_invalid(self):
        with pytest.raises(ValidationError):
            ExerciseCreate(name="", muscle_group=MuscleGroup.chest)

    def test_name_too_long_invalid(self):
        with pytest.raises(ValidationError):
            ExerciseCreate(name="a" * 101, muscle_group=MuscleGroup.chest)

    def test_name_100_chars_valid(self):
        record = ExerciseCreate(name="a" * 100, muscle_group=MuscleGroup.chest)
        assert len(record.name) == 100

    def test_invalid_muscle_group(self):
        with pytest.raises(ValidationError):
            ExerciseCreate(name="種目", muscle_group="invalid_group")

    def test_calories_negative_invalid(self):
        with pytest.raises(ValidationError):
            ExerciseCreate(name="種目", muscle_group=MuscleGroup.chest, calories_per_rep_per_kg=-0.001)

    def test_calories_zero_valid(self):
        record = ExerciseCreate(name="種目", muscle_group=MuscleGroup.chest, calories_per_rep_per_kg=0.0)
        assert record.calories_per_rep_per_kg == 0.0


class TestExerciseResponseFromDynamo:
    def test_full_item(self):
        item = {
            "exerciseId": "ex-uuid-001",
            "name": "ベンチプレス",
            "muscleGroup": "chest",
            "caloriesPerRepPerKg": Decimal("0.050"),
            "createdAt": "2026-04-25T00:00:00+00:00",
            "updatedAt": "2026-04-25T01:00:00+00:00",
        }
        response = ExerciseResponse.from_dynamo(item)
        assert response.exercise_id == "ex-uuid-001"
        assert response.name == "ベンチプレス"
        assert response.muscle_group == MuscleGroup.chest
        assert response.calories_per_rep_per_kg == 0.05
        assert response.created_at == "2026-04-25T00:00:00+00:00"
        assert response.updated_at == "2026-04-25T01:00:00+00:00"

    def test_item_without_calories(self):
        item = {
            "exerciseId": "ex-uuid-002",
            "name": "スクワット",
            "muscleGroup": "leg",
            "createdAt": "2026-04-25T00:00:00+00:00",
            "updatedAt": "2026-04-25T00:00:00+00:00",
        }
        response = ExerciseResponse.from_dynamo(item)
        assert response.calories_per_rep_per_kg is None


class TestExerciseListResponse:
    def test_empty_list(self):
        response = ExerciseListResponse(items=[])
        assert response.items == []

    def test_multiple_items(self):
        items = [
            ExerciseResponse(
                exercise_id="ex-001",
                name="ベンチプレス",
                muscle_group=MuscleGroup.chest,
                calories_per_rep_per_kg=0.05,
                created_at="2026-04-25T00:00:00+00:00",
                updated_at="2026-04-25T00:00:00+00:00",
            ),
            ExerciseResponse(
                exercise_id="ex-002",
                name="スクワット",
                muscle_group=MuscleGroup.leg,
                calories_per_rep_per_kg=None,
                created_at="2026-04-25T00:00:00+00:00",
                updated_at="2026-04-25T00:00:00+00:00",
            ),
        ]
        response = ExerciseListResponse(items=items)
        assert len(response.items) == 2
        assert response.items[0].name == "ベンチプレス"
        assert response.items[1].calories_per_rep_per_kg is None
