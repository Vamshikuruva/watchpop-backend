from ...auth.password import hash_password
from ...db.user_store import create_user, get_user_by_email

def register_user(email, password, name=None):
    if get_user_by_email(email):
        raise ValueError("User already exists")

    return create_user(
        email=email,
        password_hash=hash_password(password),
        provider="email",
        name=name,
    )
