from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user, get_dynamodb
from app.repositories.weight import WeightRepository
from app.schemas.weight import WeightRecordCreate, WeightRecordListResponse, WeightRecordResponse

router = APIRouter(prefix="/workout/weight", tags=["workout"])


def _get_repo(dynamodb=Depends(get_dynamodb)) -> WeightRepository:
    return WeightRepository(dynamodb)


@router.post("", response_model=WeightRecordResponse)
async def upsert_weight(
    body: WeightRecordCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    repo: Annotated[WeightRepository, Depends(_get_repo)],
) -> WeightRecordResponse:
    item = await repo.upsert(
        user_id=current_user["user_id"],
        record_date=body.record_date,
        weight_kg=body.weight_kg,
        body_fat_pct=body.body_fat_pct,
    )
    return WeightRecordResponse.from_dynamo(item)


@router.get("", response_model=WeightRecordListResponse)
async def list_weight(
    current_user: Annotated[dict, Depends(get_current_user)],
    repo: Annotated[WeightRepository, Depends(_get_repo)],
    from_date: str | None = None,
    to_date: str | None = None,
) -> WeightRecordListResponse:
    items = await repo.list_by_user(
        user_id=current_user["user_id"],
        from_date=from_date,
        to_date=to_date,
    )
    return WeightRecordListResponse(items=[WeightRecordResponse.from_dynamo(i) for i in items])


@router.delete("/{record_date}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_weight(
    record_date: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    repo: Annotated[WeightRepository, Depends(_get_repo)],
) -> None:
    deleted = await repo.delete(
        user_id=current_user["user_id"],
        record_date=record_date,
    )
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
