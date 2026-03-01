from pydantic import BaseModel
from typing import List, Optional

class MovieUpdateRequest(BaseModel):
    watched: Optional[bool] = None
    rating: Optional[int] = None
    my_tags: Optional[str] = None
