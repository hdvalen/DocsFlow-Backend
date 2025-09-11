from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database.database import get_db
from app.controllers.users.UsersController import UsersController
from app.schemas.Users.UsersSchema import UserRegisterRequest

router = APIRouter()

@router.post("/register")
def register_user(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    # No se requiere current_user
    return UsersController.register_user(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        db=db,
        role_name=user_data.role  # opcional, si quieres permitir que manden el rol (normalmente ignorado)
    )

