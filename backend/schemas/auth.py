from pydantic import BaseModel


class AuthUser(BaseModel):
    sub: str
    email: str
    name: str
