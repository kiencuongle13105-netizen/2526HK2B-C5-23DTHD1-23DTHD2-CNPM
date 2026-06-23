from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
