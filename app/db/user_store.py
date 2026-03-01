import uuid
from typing import Optional
from app.db.chroma import client

_USERS = client.get_or_create_collection("users")


def get_user_by_email(email: str) -> Optional[dict]:
    result = _USERS.get(
        where={"email": email},
        limit=1
    )

    if not result["ids"]:
        return None

    return {
        "id": result["ids"][0],
        **result["metadatas"][0],
    }



def get_user_by_id(user_id: str) -> Optional[dict]:
    result = _USERS.get(ids=[user_id])

    if not result["ids"]:
        return None

    return {
        "id": result["ids"][0],
        **result["metadatas"][0],
    }


def create_user(email, provider, password_hash=None, name=None):
    if get_user_by_email(email):
        raise ValueError("User with this email already exists")

    user_id = str(uuid.uuid4())

    metadata = {
        "email": email,
        "provider": provider,
        "password_hash": password_hash,
        "name": name,
    }

    # 🔥 Remove None values
    metadata = {k: v for k, v in metadata.items() if v is not None}

    _USERS.add(
        ids=[user_id],
        documents=[email],
        metadatas=[metadata]
    )

    return {
        "id": user_id,
        "email": email,
        "provider": provider,
        "password_hash": password_hash,
        "name": name,
    }




def get_or_create_google_user(email, name):
    user = get_user_by_email(email)
    if user:
        return user
    return create_user(email=email, provider="google", name=name)
