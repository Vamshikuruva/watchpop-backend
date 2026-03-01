from fastapi import APIRouter, HTTPException, Depends, Response, Request
from app.schemas.auth.register import RegisterSchema
from app.schemas.auth.login import LoginSchema
from app.schemas.auth.google import GoogleTokenRequest
from app.services.auth.user_create import register_user
from app.services.auth.user_login import login_user
from app.services.auth.google_login import google_login
from app.auth.jwt import create_access_token, create_refresh_token, decode_token
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

REFRESH_COOKIE_NAME = "refresh_token"


def set_refresh_cookie(response: Response, refresh_token: str):
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=False,  # set False only for local dev if needed
        samesite="lax",
        max_age=60 * 60 * 24 * 30,  # 30 days
        path="/auth",
    )

ACCESS_COOKIE_NAME = "access_token"

def set_access_cookie(response: Response, access_token: str):
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=False,  # False for local dev only
        samesite="lax",
        max_age=60 * 15,  # 15 minutes
        path="/",
    )

@router.post("/register")
def register(data: RegisterSchema, response: Response):
    try:
        user = register_user(data.email, data.password, data.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    access_token = create_access_token(user["id"])
    refresh_token = create_refresh_token(user["id"])

    set_access_cookie(response, access_token)
    set_refresh_cookie(response, refresh_token)

    return {"message": "Login successful"}


@router.post("/login")
def login(data: LoginSchema, response: Response):
    try:
        user = login_user(data.email, data.password)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user["id"])
    refresh_token = create_refresh_token(user["id"])

    set_access_cookie(response, access_token)
    set_refresh_cookie(response, refresh_token)

    return {"message": "Login successful"}


@router.post("/google")
def google_auth(data: GoogleTokenRequest, response: Response):
    user = google_login(data.token)

    access_token = create_access_token(user["id"])
    refresh_token = create_refresh_token(user["id"])

    set_access_cookie(response, access_token)
    set_refresh_cookie(response, refresh_token)

    return {"message": "Login successful"}


@router.post("/refresh")
def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = decode_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    access_token = create_access_token(user_id)
    set_access_cookie(response, access_token)

    return {"message": "Token refreshed"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(REFRESH_COOKIE_NAME, path="/auth")
    return {"message": "Logged out successfully"}


@router.get("/me")
def get_profile(user=Depends(get_current_user)):
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "profile_picture": user.get("picture") or "",
        "provider": user.get("provider"),
    }
