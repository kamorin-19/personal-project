from decimal import Decimal

from pydantic import BaseModel, Field


class CalorieLogCreate(BaseModel):
    record_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    calories: int = Field(ge=0, le=99999)


class CalorieLogResponse(BaseModel):
    record_date: str
    calories: int
    created_at: str
    updated_at: str

    @classmethod
    def from_dynamo(cls, item: dict) -> "CalorieLogResponse":
        return cls(
            record_date=item["recordDate"],
            calories=int(item["calories"]),
            created_at=item["createdAt"],
            updated_at=item["updatedAt"],
        )


class CalorieLogListResponse(BaseModel):
    items: list[CalorieLogResponse]
