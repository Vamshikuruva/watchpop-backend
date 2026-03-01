from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt import decode_token
from app.db.user_store import get_user_by_id

security = HTTPBearer(auto_error=False)  # 🔥 important


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = None

    # 1️⃣ Try cookie first
    token = request.cookies.get("access_token")

    # 2️⃣ Fallback to Authorization header (Swagger support)
    if not token and credentials:
        token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

security_optional = HTTPBearer(auto_error=False)

def get_current_user_optional(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security_optional),
):
    token = None

    # 1️⃣ Try cookie first (SSR fix)
    token = request.cookies.get("access_token")

    # 2️⃣ Fallback to Authorization header (Swagger support)
    if not token and credentials:
        token = credentials.credentials

    if not token:
        return None

    payload = decode_token(token)
    if not payload:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    return get_user_by_id(user_id)