from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class UserEntry(BaseModel):
    watched: Optional[bool] = None # movie
    listened: Optional[bool] = None # music
    rating: Optional[float] = None
    friends_recommended: Optional[str] = None
    my_tags: Optional[str] = None


class FullMediaResponse(BaseModel):
    type: str
    id: str

    title: Optional[str] = None
    subtitle: Optional[str] = None
    poster: Optional[str] = None
    genre: Optional[str] = None
    release_date: Optional[str] = None
    description: Optional[str] = None

    provider_data: Dict[str, Any]

    user_entry: Optional[UserEntry] = None