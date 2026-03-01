from pydantic import BaseModel
from typing import List, Optional

class SongAddRequest(BaseModel):
    track_id: str
    friends_recommended: List[str] = []
    listened: bool = False
    rating: Optional[int] = None
