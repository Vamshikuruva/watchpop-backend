from pydantic import BaseModel
from typing import List, Optional

class MovieAddRequest(BaseModel):
    imdb_id: str
    friends_recommended: List[str] = []
    watched: Optional[bool] = False
    rating: Optional[int] = None
