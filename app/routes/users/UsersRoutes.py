from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.database import get_db
from app.controllers.users.UsersController import UsersController

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):
    return UsersController.register_user(name, email, password, db)

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    return UsersController.login_user(email, password, db)
