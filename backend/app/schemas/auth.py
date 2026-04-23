from pydantic import BaseModel


class GoogleCallbackRequest(BaseModel):
    code: str
    code_verifier: str


class TokenResponse(BaseModel):
    token: str


class UserInfo(BaseModel):
    user_id: str
    email: str
    name: str | None = None
