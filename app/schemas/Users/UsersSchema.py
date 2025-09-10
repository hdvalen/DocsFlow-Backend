from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"  # <- por defecto user


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    company_id: Optional[int] = None
    department_id: Optional[int] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse