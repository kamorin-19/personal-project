from decimal import Decimal
from pydantic import BaseModel, Field


class WeightRecordCreate(BaseModel):
    record_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    weight_kg: float = Field(gt=0, le=300)
    body_fat_pct: float | None = Field(default=None, ge=0, le=100)


class WeightRecordResponse(BaseModel):
    record_date: str
    weight_kg: float
    body_fat_pct: float | None
    created_at: str
    updated_at: str

    @classmethod
    def from_dynamo(cls, item: dict) -> "WeightRecordResponse":
        return cls(
            record_date=item["recordDate"],
            weight_kg=float(item["weightKg"]),
            body_fat_pct=float(item["bodyFatPct"]) if "bodyFatPct" in item else None,
            created_at=item["createdAt"],
            updated_at=item["updatedAt"],
        )


class WeightRecordListResponse(BaseModel):
    items: list[WeightRecordResponse]
