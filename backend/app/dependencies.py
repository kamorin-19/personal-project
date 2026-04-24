from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Annotated

import aioboto3
from aioboto3 import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import settings

if TYPE_CHECKING:
    from types_aiobotocore_dynamodb import DynamoDBServiceResource


_session: Session = aioboto3.Session()
_bearer = HTTPBearer()


async def get_dynamodb() -> AsyncGenerator["DynamoDBServiceResource", None]:
    async with _session.resource(
        "dynamodb",
        endpoint_url=settings.dynamodb_endpoint_url,
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    ) as dynamodb:
        yield dynamodb


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer)],
) -> dict:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {
            "user_id": user_id,
            "email": payload.get("email", ""),
            "name": payload.get("name"),
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
