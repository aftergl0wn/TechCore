import os
from http import HTTPStatus

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

load_dotenv(".env")


security = HTTPBearer()


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token, os.getenv("JWT_SECRET_KEY"),
            algorithms=[os.getenv("JWT_ALGORITHM")]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid token"
        )


def require_role(required_role: str):

    async def check_role(token_payload: dict = Depends(verify_token)):
        role = token_payload.get("role") or token_payload.get("scope")

        if not role:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Forbidden: role or scope not found in token"
            )

        if isinstance(role, list):
            has_role = required_role in role
        else:
            has_role = role == required_role

        if not has_role:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail=f"Required role '{required_role}' not found"
            )

        return token_payload

    return check_role
