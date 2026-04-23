import asyncio
import logging
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import httpx
from fastapi import APIRouter, HTTPException
from jose import jwt

from app.config import settings
from app.schemas.auth import GoogleCallbackRequest, TokenResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


async def _exchange_code(code: str, code_verifier: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            GOOGLE_TOKEN_ENDPOINT,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "code_verifier": code_verifier,
                "redirect_uri": settings.google_redirect_uri,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
            },
        )
        resp.raise_for_status()
        return resp.json()


def _verify_id_token_sync(id_token_str: str) -> dict:
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests

    idinfo = id_token.verify_oauth2_token(
        id_token_str,
        google_requests.Request(),
        settings.google_client_id,
    )
    if idinfo["iss"] not in ("accounts.google.com", "https://accounts.google.com"):
        raise ValueError("Invalid token issuer")
    return {
        "google_id": idinfo["sub"],
        "email": idinfo["email"],
        "name": idinfo.get("name"),
    }


async def _verify_id_token(id_token_str: str) -> dict:
    return await asyncio.to_thread(_verify_id_token_sync, id_token_str)


def _create_session_token(user_id: str, email: str, name: str | None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "email": email,
        "name": name,
        "jti": str(uuid4()),
        "iat": now,
        "exp": now + timedelta(hours=settings.jwt_expire_hours),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


async def _upsert_user(google_id: str, email: str, name: str | None) -> dict:
    """DynamoDB にユーザーをアップサート。テーブル未作成時はスキップ。"""
    try:
        import aioboto3
        from botocore.exceptions import ClientError

        session = aioboto3.Session()
        kwargs: dict = {"region_name": settings.aws_region}
        if settings.dynamodb_endpoint_url:
            kwargs["endpoint_url"] = settings.dynamodb_endpoint_url

        async with session.resource("dynamodb", **kwargs) as dynamodb:
            table = await dynamodb.Table("users")
            await table.put_item(
                Item={
                    "userId": google_id,
                    "email": email,
                    "name": name or "",
                    "updatedAt": datetime.now(timezone.utc).isoformat(),
                },
                ConditionExpression="attribute_not_exists(userId) OR attribute_exists(userId)",
            )
    except Exception as e:
        logger.warning("DynamoDB upsert skipped: %s", e)

    return {"userId": google_id, "email": email, "name": name}


@router.post("/google/callback", response_model=TokenResponse)
async def google_callback(req: GoogleCallbackRequest) -> TokenResponse:
    try:
        token_data = await _exchange_code(req.code, req.code_verifier)
    except httpx.HTTPStatusError as e:
        logger.error("Google token exchange failed: %s", e.response.text)
        raise HTTPException(status_code=400, detail="Google token exchange failed")

    id_token_str = token_data.get("id_token")
    if not id_token_str:
        raise HTTPException(status_code=400, detail="ID token not found in Google response")

    try:
        user_info = await _verify_id_token(id_token_str)
    except Exception as e:
        logger.error("ID token verification failed: %s", e)
        raise HTTPException(status_code=401, detail="Invalid Google ID token")

    user = await _upsert_user(
        google_id=user_info["google_id"],
        email=user_info["email"],
        name=user_info["name"],
    )

    token = _create_session_token(
        user_id=user["userId"],
        email=user["email"],
        name=user["name"],
    )
    return TokenResponse(token=token)
