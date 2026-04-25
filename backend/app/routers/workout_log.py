from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user, get_dynamodb
from app.repositories.workout_log import WorkoutLogRepository
from app.schemas.workout_log import WorkoutLogCreate, WorkoutLogListResponse, WorkoutLogResponse

router = APIRouter(prefix="/workout/log", tags=["workout"])


def _get_repo(dynamodb=Depends(get_dynamodb)) -> WorkoutLogRepository:
    return WorkoutLogRepository(dynamodb)


@router.post("", response_model=WorkoutLogResponse, status_code=status.HTTP_201_CREATED)
async def create_log(
    body: WorkoutLogCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    repo: Annotated[WorkoutLogRepository, Depends(_get_repo)],
) -> WorkoutLogResponse:
    item = await repo.create(
        user_id=current_user["user_id"],
        record_date=body.record_date,
        exercise_id=body.exercise_id,
        exercise_name=body.exercise_name,
        weight_kg=body.weight_kg,
        sets=body.sets,
    )
    return WorkoutLogResponse.from_dynamo(item)


@router.get("", response_model=WorkoutLogListResponse)
async def list_logs(
    current_user: Annotated[dict, Depends(get_current_user)],
    repo: Annotated[WorkoutLogRepository, Depends(_get_repo)],
    from_date: str | None = None,
    to_date: str | None = None,
) -> WorkoutLogListResponse:
    items = await repo.list_by_user(
        user_id=current_user["user_id"],
        from_date=from_date,
        to_date=to_date,
    )
    return WorkoutLogListResponse(items=[WorkoutLogResponse.from_dynamo(i) for i in items])


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(
    log_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    repo: Annotated[WorkoutLogRepository, Depends(_get_repo)],
) -> None:
    deleted = await repo.delete(
        user_id=current_user["user_id"],
        log_id=log_id,
    )
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")
