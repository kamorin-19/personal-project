from enum import Enum

from pydantic import BaseModel, Field


class MuscleGroup(str, Enum):
    chest = "chest"
    back = "back"
    shoulder = "shoulder"
    arm = "arm"
    abdomen = "abdomen"
    leg = "leg"
    other = "other"


class ExerciseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    muscle_group: MuscleGroup
    calories_per_rep_per_kg: float | None = Field(default=None, ge=0)


class ExerciseResponse(BaseModel):
    exercise_id: str
    name: str
    muscle_group: MuscleGroup
    calories_per_rep_per_kg: float | None
    created_at: str
    updated_at: str

    @classmethod
    def from_dynamo(cls, item: dict) -> "ExerciseResponse":
        return cls(
            exercise_id=item["exerciseId"],
            name=item["name"],
            muscle_group=item["muscleGroup"],
            calories_per_rep_per_kg=float(item["caloriesPerRepPerKg"])
            if "caloriesPerRepPerKg" in item
            else None,
            created_at=item["createdAt"],
            updated_at=item["updatedAt"],
        )


class ExerciseListResponse(BaseModel):
    items: list[ExerciseResponse]
