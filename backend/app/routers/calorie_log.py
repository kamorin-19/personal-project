from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user, get_dynamodb
from app.repositories.calorie_log import CalorieLogRepository
from app.schemas.calorie_log import CalorieLogCreate, CalorieLogListResponse, CalorieLogResponse

router = APIRouter(prefix="/workout/calorie", tags=["workout"])


def _get_repo(dynamodb=Depends(get_dynamodb)) -> CalorieLogRepository:
    return CalorieLogRepository(dynamodb)


@router.post("", response_model=CalorieLogResponse)
async def upsert_calorie(
    body: CalorieLogCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    repo: Annotated[CalorieLogRepository, Depends(_get_repo)],
) -> CalorieLogResponse:
    item = await repo.upsert(
        user_id=current_user["user_id"],
        record_date=body.record_date,
        calories=body.calories,
    )
    return CalorieLogResponse.from_dynamo(item)


@router.get("", response_model=CalorieLogListResponse)
async def list_calorie(
    current_user: Annotated[dict, Depends(get_current_user)],
    repo: Annotated[CalorieLogRepository, Depends(_get_repo)],
    from_date: str | None = None,
    to_date: str | None = None,
) -> CalorieLogListResponse:
    items = await repo.list_by_user(
        user_id=current_user["user_id"],
        from_date=from_date,
        to_date=to_date,
    )
    return CalorieLogListResponse(items=[CalorieLogResponse.from_dynamo(i) for i in items])


@router.delete("/{record_date}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_calorie(
    record_date: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    repo: Annotated[CalorieLogRepository, Depends(_get_repo)],
) -> None:
    deleted = await repo.delete(
        user_id=current_user["user_id"],
        record_date=record_date,
    )
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
