from pydantic import BaseModel
from typing import List, Optional

class SongUpdateRequest(BaseModel):
    listened: Optional[bool] = None
    rating: Optional[int] = None
    my_tags: Optional[List[str]] = None