from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user, get_dynamodb
from app.repositories.exercise import ExerciseRepository
from app.schemas.exercise import ExerciseCreate, ExerciseListResponse, ExerciseResponse

router = APIRouter(prefix="/workout/exercise", tags=["workout"])


def _get_repo(dynamodb=Depends(get_dynamodb)) -> ExerciseRepository:
    return ExerciseRepository(dynamodb)


@router.post("", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    body: ExerciseCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    repo: Annotated[ExerciseRepository, Depends(_get_repo)],
) -> ExerciseResponse:
    item = await repo.create(
        user_id=current_user["user_id"],
        name=body.name,
        muscle_group=body.muscle_group.value,
        calories_per_rep_per_kg=body.calories_per_rep_per_kg,
    )
    return ExerciseResponse.from_dynamo(item)


@router.get("", response_model=ExerciseListResponse)
async def list_exercises(
    current_user: Annotated[dict, Depends(get_current_user)],
    repo: Annotated[ExerciseRepository, Depends(_get_repo)],
) -> ExerciseListResponse:
    items = await repo.list_by_user(user_id=current_user["user_id"])
    return ExerciseListResponse(items=[ExerciseResponse.from_dynamo(i) for i in items])


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(
    exercise_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    repo: Annotated[ExerciseRepository, Depends(_get_repo)],
) -> None:
    deleted = await repo.delete(
        user_id=current_user["user_id"],
        exercise_id=exercise_id,
    )
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
