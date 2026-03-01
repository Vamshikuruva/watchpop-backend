from ...auth.password import verify_password
from ...db.user_store import get_user_by_email

def login_user(email, password):
    user = get_user_by_email(email)
    if not user or not user["password_hash"]:
        raise ValueError("Invalid credentials")

    if not verify_password(password, user["password_hash"]):
        raise ValueError("Invalid credentials")

    return user
