from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.database import get_db
from app.controllers.users.UsersController import UsersController
from app.auth.dependencies import get_current_user_optional

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")  
def register_user(
    name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_optional)  # opción JWT
):
    return UsersController.register_user(name, email, password, db, current_user)
