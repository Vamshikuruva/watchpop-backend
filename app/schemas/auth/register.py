from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None
