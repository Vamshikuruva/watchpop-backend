from pydantic import BaseModel

class GoogleTokenRequest(BaseModel):
    token: str
