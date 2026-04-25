from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class WorkoutLogCreate(BaseModel):
    record_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    exercise_id: str = Field(min_length=1)
    exercise_name: str = Field(min_length=1, max_length=100)
    weight_kg: float | None = Field(default=None, ge=0, le=999)
    sets: list[int] = Field(min_length=1, max_length=10)

    @field_validator("sets")
    @classmethod
    def sets_must_be_non_negative(cls, v: list[int]) -> list[int]:
        if any(s < 0 for s in v):
            raise ValueError("reps must be non-negative")
        return v


class WorkoutLogResponse(BaseModel):
    log_id: str
    record_date: str
    exercise_id: str
    exercise_name: str
    weight_kg: float | None
    sets: list[int]
    created_at: str
    updated_at: str

    @classmethod
    def from_dynamo(cls, item: dict) -> "WorkoutLogResponse":
        return cls(
            log_id=item["logId"],
            record_date=item["recordDate"],
            exercise_id=item["exerciseId"],
            exercise_name=item["exerciseName"],
            weight_kg=float(item["weightKg"]) if "weightKg" in item else None,
            sets=[int(s) for s in item["sets"]],
            created_at=item["createdAt"],
            updated_at=item["updatedAt"],
        )


class WorkoutLogListResponse(BaseModel):
    items: list[WorkoutLogResponse]
