from ...auth.google_oauth import verify_google_token
from ...db.user_store import get_or_create_google_user

def google_login(id_token_str: str):
    payload = verify_google_token(id_token_str)

    return get_or_create_google_user(
        email=payload["email"] or "Email not provided",
        name=payload.get("name") or "User",
    )
